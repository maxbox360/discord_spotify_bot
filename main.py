import discord
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
import re
import os

intents = discord.Intents.default()
intents.messages = True
client = discord.Client(intents=intents)

# Initialize Spotify API
spotify_client_id = 'YOUR_SPOTIFY_CLIENT_ID'
spotify_client_secret = 'YOUR_SPOTIFY_CLIENT_SECRET'
spotify_redirect_uri = 'http://localhost:8888/callback'  # Must match your Spotify app's redirect URI
scope = 'playlist-modify-public playlist-modify-private'

sp = Spotify(auth_manager=SpotifyOAuth(client_id=spotify_client_id,
                                      client_secret=spotify_client_secret,
                                      redirect_uri=spotify_redirect_uri,
                                      scope=scope))

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if 'spotify.com/track/' in message.content:
        song_link = extract_spotify_link(message.content)
        if song_link:
            result = add_song_to_playlist(song_link)
            if result:
                await message.channel.send("Song successfully added to the playlist!")
            else:
                await message.channel.send("Failed to add the song to the playlist.")

def extract_spotify_link(text):
    pattern = r'https://open\.spotify\.com/track/[a-zA-Z0-9]+'
    match = re.search(pattern, text)
    if match:
        return match.group()
    return None

def add_song_to_playlist(song_link):
    track_id = song_link.split('/')[-1]  # Extract track ID from Spotify link
    playlist_id = 'YOUR_PLAYLIST_ID'  # Replace with your playlist ID

    try:
        sp.playlist_add_items(playlist_id, [f'spotify:track:{track_id}'])
        return True
    except Exception as e:
        print(f"Error adding song to playlist: {e}")
        return False

client.run('YOUR_DISCORD_BOT_TOKEN')

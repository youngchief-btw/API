import base64, json, os, sched, sqlite3, time, aiohttp
import os, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.insert(0, currentdir)
import sqlite as sql

spotifyClientId = os.environ.get('SPOTIFY_CLIENT_ID')
spotifyClientSecret = os.environ.get('SPOTIFY_CLIENT_SECRET')
spotifyRedirectUri = os.environ.get('SPOTIFY_REDIRECT_URI')
spotifyUserId = os.environ.get('SPOTIFY_USER_ID')
spotifyAccessToken = None 
if sql.read("SPOTIFY_REFRESH_TOKEN"):
  spotifyRefreshToken = sql.read("SPOTIFY_REFRESH_TOKEN")
else: 
  spotifyRefreshToken = None

async def refreshAccessToken():
    global spotifyRefreshToken
    if not spotifyRefreshToken:
        return None
    auth_header = base64.b64encode(
        f"{spotifyClientId}:{spotifyClientSecret}".encode('utf-8')).decode('utf-8')
    data = {'grant_type': 'refresh_token', 'refresh_token': spotifyRefreshToken}
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': f'Basic {auth_header}'
    }
    async with aiohttp.ClientSession() as session:
        async with session.post('https://accounts.spotify.com/api/token',
                                 data=data,
                                 headers=headers) as response:
            response_data = await response.json()
            access = response_data.get('access_token')
            sql.set("SPOTIFY_ACCESS_TOKEN", access)
            spotifyAccessToken = access
            return access
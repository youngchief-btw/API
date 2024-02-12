import base64
import os
import aiohttp

# Import the wrappers
from db_spotify import set as db_set
from db_spotify import get as db_get

# Set important variables
env = os.environ

spotifyClientId = env['SPOTIFY_CLIENT_ID']
spotifyClientSecret = env['SPOTIFY_CLIENT_SECRET']
spotifyRedirectUri = env['SPOTIFY_REDIRECT_URI']
spotifyUserId = env['SPOTIFY_USER_ID']
spotifyAccessToken = None

# Check if the refresh token is set in the database, if not, fail gracefully
if db_get('refresh_token'):
    spotifyRefreshToken = db_get('refresh_token')
else:
    spotifyRefreshToken = None

# Renew the access token with the refresh token
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
            if 'error' in response_data:
                print(f"Error refreshing access token: {response_data['error']}")
                return None
            access = response_data.get('access_token')
            if not access:
                print("No access token received.")
                return None
            # Set access token in the database
            db_set('access_token', access)
            return access


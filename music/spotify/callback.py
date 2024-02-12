import os
import aiohttp
import base64

# Import the Postgres wrappers
from db_spotify import set as db_set
from db_spotify import get as db_get

env = os.environ

spotifyClientId = env['SPOTIFY_CLIENT_ID']
spotifyClientSecret = env['SPOTIFY_CLIENT_SECRET']
spotifyRedirectUri = env['SPOTIFY_REDIRECT_URI']
spotifyUserId = env['SPOTIFY_USER_ID']
spotifyAccessToken = None

if db_get('refresh_token'):
    spotifyRefreshToken = db_get('refresh_token')
else:
    spotifyRefreshToken = None

async def callback(request):
    print(f'/spotify/callback: Authorization Code { request.args.get("code") }')
    auth_header = base64.b64encode(
        f"{spotifyClientId}:{spotifyClientSecret}".encode('utf-8')).decode('utf-8')
    data = {
        'grant_type': 'authorization_code',
        'code': request.args.get('code'),
        'redirect_uri': spotifyRedirectUri
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': f'Basic {auth_header}'
    }

    async with aiohttp.ClientSession() as session:
        async with session.post('https://accounts.spotify.com/api/token',
                                data=data,
                                headers=headers) as response:
            response_data = await response.json()
            print('/spotify/callback: Exchange authorization code for refresh and access tokens')
            print(response_data)

            try:
                access_token = response_data['access_token']
                refresh_token = response_data['refresh_token']

                headers = {'Authorization': 'Bearer ' + access_token}
                async with session.get('https://api.spotify.com/v1/me', headers=headers) as response:
                    user_id = (await response.json()).get('id')
                    if user_id != spotifyUserId:
                        return {'error': 'Unauthorized'}

                db_set('refresh_token', refresh_token)
                db_set('access_token', access_token)
                return refresh_token

            except KeyError as e:
                print(f"Error: Missing key in response data: {e}")
                return {'error': 'Invalid token response'}
            except aiohttp.ClientError as e:
                print(f"Error: Network error: {e}")
                return {'error': 'Network error'}


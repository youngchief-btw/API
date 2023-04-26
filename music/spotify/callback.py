# /spotify/callback
# IMPORTING THINGS
import os, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.insert(0, currentdir)
import sqlite as sql
# I'm totally fine.
import aiohttp
async def callback(request):
    global spotifyAccessToken
    global spotifyRefreshToken
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
                                   
            spotifyAccessToken = response_data['access_token']
            os.environ['SPOTIFY_ACCESS_TOKEN'] = spotifyAccessToken
                                   
            spotifyRefreshToken = response_data['refresh_token']
            os.environ['SPOTIFY_REFRESH_TOKEN'] = spotifyRefreshToken
                                   
            headers = {'Authorization': 'Bearer ' + spotifyAccessToken}
            async with session.get('https://api.spotify.com/v1/me', headers=headers) as response:
                user_data = await response.json()
                user_id = user_data.get('id')
                if user_id != spotifyUserId:
                    return {'error': 'Unauthorized'}
                #else: 
                    #set("SPOTIFY_REFRESH_TOKEN", spotifyRefreshToken)

  
    sql.set("SPOTIFY_REFRESH_TOKEN", spotifyRefreshToken)
    return spotifyRefreshToken #'Authenticated!'
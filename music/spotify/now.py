import os, sys, inspect, aiohttp
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.insert(0, currentdir)
from db_spotify import set as db_set
from db_spotify import get as db_get
import auth
import json

async def now():
    spotifyAccessToken = db_get('access_token')
    spotifyRefreshToken = db_get('refresh_token')

    if spotifyAccessToken is None:
        spotifyAccessToken = await auth.refreshAccessToken()
        if spotifyAccessToken is None:
            return {'error': 'Access token not found'}

    headers = {'Authorization': f'Bearer {spotifyAccessToken}'}
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get('https://api.spotify.com/v1/me/player', headers=headers) as resp:
                if resp.status !=  200:
                    return {'error': 'Failed to retrieve now playing data from Spotify.'}
                d = await resp.json()
    except Exception as e:
        return {'error': f'An error occurred while retrieving data from Spotify: {str(e)}'}

    if not d.get('is_playing') or not d.get('item'):
        return {'error': 'No data available for currently playing track.'}

    reply = {
        'playing': d.get('is_playing', False),
        'progress': d.get('progress_ms',  0),
        'isrc': d['item']['external_ids'].get('isrc', ''),
        'timestamp': d.get('timestamp',  0),
    }
    finalReply = json.dumps(reply, separators=(',', ':'))
    print(finalReply)
    return finalReply


#async def now():
    #global spotifyAccessToken
    #spotifyAccessToken = db_get('access_token')
    #global spotifyRefreshToken
    #spotifyRefreshToken = db_get('refresh_token')
    #spotifyAccessToken = None
    #if spotifyAccessToken is None:
        #spotifyAccessToken = await auth.refreshAccessToken()
        #if spotifyAccessToken is None:
            #       return {'error': 'Access token not found'}

    #headers = {'Authorization': 'Bearer ' + spotifyAccessToken}
    #async with aiohttp.ClientSession(headers=headers) as session:
        #async with session.get('https://api.spotify.com/v1/me/player') as resp:
            #if resp.status != 200:
                #          return {'error': 'Failed to retrieve now playing data from Spotify.'}
     #       d = await resp.json()

    #if not d.get('is_playing') or not d.get('item'):
        #   return {'error': 'No data available for currently playing track.'}

    #reply = {
            #'playing': d.get('is_playing', False),
        #'progress': d.get('progress_ms', 0),
        #'isrc': d['item']['external_ids'].get('isrc', ''),
        #'timestamp': d.get('timestamp', 0),
        #    }
#    finalReply = json.dumps(reply, separators=(',', ':')) or '{}' #.replace('"', "'") or '{}'
#    print(finalReply)
#    return finalReply or {}

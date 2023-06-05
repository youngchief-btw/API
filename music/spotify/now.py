import os, sys, inspect, aiohttp
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.insert(0, currentdir)
import auth
import sqlite as sql
import json
async def now():
    global spotifyAccessToken
    global spotifyRefreshToken
    spotifyAccessToken = None
    if spotifyAccessToken is None:
        spotifyAccessToken = await auth.refreshAccessToken()
        if spotifyAccessToken is None:
            return {'error': 'Access token not found'}

    headers = {'Authorization': 'Bearer ' + spotifyAccessToken}
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get('https://api.spotify.com/v1/me/player') as resp:
            if resp.status != 200:
                return {'error': 'Failed to retrieve now playing data from Spotify.'}
            d = await resp.json()

    if not d.get('is_playing') or not d.get('item'):
        return {'error': 'No data available for currently playing track.'}

    reply = {
        'playing': d.get('is_playing', False),
        'progress': d.get('progress_ms', 0),
        'isrc': d['item']['external_ids'].get('isrc', ''),
        'timestamp': d.get('timestamp', 0),
    }
    finalReply = json.dumps(reply, separators=(',', ':')) or '{}' #.replace('"', "'") or '{}'
    print(finalReply)
    return finalReply or {}

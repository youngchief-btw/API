import json
import aiohttp
import auth
async def history():
    global spotifyAccessToken
    global spotifyRefreshToken
    spotifyAccessToken = None
    if spotifyAccessToken is None:
        spotifyAccessToken = await auth.refreshAccessToken()
        if spotifyAccessToken is None:
            return {'error': 'Access token not found'}
    
    headers = {'Authorization': 'Bearer ' + spotifyAccessToken}
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get('https://api.spotify.com/v1/me/player/recently-played?limit=50') as resp:
            if resp.status != 200:
                # print(resp.status)
                return {'error': 'Failed to retrieve history data from Spotify.'}
            d = await resp.json()

    isrcs = {"history": []}
    index = 0
    for item in d["items"]:
        if "track" in item:
          isrc = item["track"]["external_ids"]["isrc"]
          isrcs["history"].append(isrc)
          index += 1
        else:
          print("No tracks in history.")

  
    finalReply = json.dumps(isrcs, separators=(',', ':')) or '{}'
    print(finalReply)
    return finalReply or {}
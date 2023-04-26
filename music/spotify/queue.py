import json
import aiohttp
import auth
async def queue():
    global spotifyAccessToken
    global spotifyRefreshToken
    spotifyAccessToken = None
    if spotifyAccessToken is None:
        spotifyAccessToken = await auth.refreshAccessToken()
        if spotifyAccessToken is None:
            return "{'error': 'Access token not found'}"
    
    headers = {'Authorization': 'Bearer ' + spotifyAccessToken}
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get('https://api.spotify.com/v1/me/player/queue') as resp:
            if resp.status != 200:
                return '{"error": "Failed to retrieve queue data from Spotify."}'
            d = await resp.json()

    isrcs = {"queue": []}
    index = 0
    for item in d["queue"]:
        if "external_ids" in item:
          isrc = item["external_ids"]["isrc"]
          isrcs["queue"].append(isrc)
          index += 1
        else: 
          print("No tracks queued.")
  
    finalReply = json.dumps(isrcs, separators=(',', ':')) or '{}'
    print(finalReply)
    return finalReply or {} #brb
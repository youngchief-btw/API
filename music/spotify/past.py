import json
import aiohttp
import auth
async def past():
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
                return {'error': 'Failed to retrieve past data from Spotify.'}
            d = await resp.json()

    isrcs = {"past": []}
    index = 0
    for item in d["items"]:
        if "track" in item:
            isrc = item["track"]["external_ids"]["isrc"]
            isrcs["past"].append(isrc)
            index += 1
            break
        else:
            print("No tracks in past.")


    finalReply = json.dumps(isrcs, separators=(',', ':')) or '{}'
    print(finalReply)
    return finalReply or {}

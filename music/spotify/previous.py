import json
import aiohttp
import auth

async def previous():
    global spotifyAccessToken
    global spotifyRefreshToken
    spotifyAccessToken = None
    if spotifyAccessToken is None:
        spotifyAccessToken = await auth.refreshAccessToken()
        if spotifyAccessToken is None:
            return "{'error': 'Access token not found'}"

    headers = {'Authorization': 'Bearer ' + spotifyAccessToken}
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get('https://api.spotify.com/v1/me/player/recently-played?limit=50') as resp:
            if resp.status != 200:
                return "{'error': 'Failed to retrieve previous track data from Spotify.'}"
            d = await resp.json()

    previous_track = None
    for item in d["items"]:
        if "track" in item:
            isrc = item["track"]["external_ids"]["isrc"]
            previous_track = isrc
            break
        else:
            print("No previous tracks.")

    isrcs = {"previous": previous_track}
    final_reply = json.dumps(isrcs, separators=(',', ':')) or '{}'
    print(final_reply)
    return final_reply or "{}"

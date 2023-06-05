import json
import aiohttp
import auth

async def next():
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
                return '{"error": "Failed to retrieve next data from Spotify."}'
            d = await resp.json()

    next_track = None
    for item in d["queue"]:
        if "external_ids" in item:
            isrc = item["external_ids"]["isrc"]
            next_track = isrc
            break
        else:
            print("No track playing next.")

    isrcs = {"next": next_track}
    final_reply = json.dumps(isrcs, separators=(',', ':')) or '{}'
    print(final_reply)
    return final_reply or "{}"

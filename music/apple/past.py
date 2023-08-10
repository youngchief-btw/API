# https://developer.apple.com/documentation/applemusicapi/get_recently_played_tracks
import os
import json
import aiohttp
# for now, grab the access token from .env
accessToken = os.environ['APPLE_MUSIC_ACCESS_TOKEN']
mediaUserToken = os.environ['APPLE_MUSIC_MEDIA_USER_TOKEN']
async def past() -> str:
    url = 'https://api.music.apple.com/v1/me/recent/played/tracks?types=library-music-videos%2Clibrary-songs%2Cmusic-videos%2Csongs'
    headers = {
        'Authorization': f'Bearer {accessToken}',
        'Media-User-Token': mediaUserToken,
        'Origin': 'https://music.apple.com'
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            data = await response.json()
            isrcs = []
            for song in data['data']:
                try:
                    isrcs.append({"type":"isrc","id":song["attributes"]["isrc"]})
                except KeyError:
                    isrcs.append({"type":"apple","id":song["attributes"]["playParams"]["catalogId"]})
            isrcDump = json.dumps(isrcs, separators=(',', ':')) or '[]'
            finalReply = '{"past":' + isrcDump + "}" if isrcDump else '{"past":[]}'
            return finalReply or '{"past":[]}'
            
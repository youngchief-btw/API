from quart import Quart, request
from music.spotify.now import now
from music.spotify.future import future
from music.spotify.next import next
from music.spotify.past import past
from music.spotify.previous import previous
from music.spotify.callback import callback as cb

app = Quart(__name__)

@app.route('/')
async def root():
    return ''

# @app.route('/spotify')
# async def slashSpotify():
#     return await now()
  
@app.route('/spotify/future')
async def slashSpotifyFuture():
    return await future()

@app.route('/spotify/past')
async def slashSpotifyPast():
    return await past()

@app.route('/spotify/callback')
async def slashSpotifyCallback():
    return await cb(request)

@app.route('/spotify/now')
async def slashSpotifyNow():
    return await now()

@app.route('/spotify/next')
async def slashSpotifyNext():
    return await next()

@app.route('/spotify/previous')
async def slashSpotifyPrevious():
    return await previous()


app.run(host='0.0.0.0', port=8080)

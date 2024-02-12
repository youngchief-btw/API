from quart import Quart, request
# Spotify Imports
from music.spotify.now import now as spotifyNow
from music.spotify.future import future as spotifyFuture
from music.spotify.next import next as spotifyNext
from music.spotify.past import past as spotifyPast
from music.spotify.previous import previous as spotifyPrevious
from music.spotify.callback import callback as spotifyCallback
# Apple Music Imports
# from music.apple.past import past as appleMusicPast
import os
env = os.environ

app = Quart(__name__)

@app.route('/')
async def root():
    return ''

# @app.route('/spotify')
# async def slashSpotify():
#     return await now()

@app.route('/spotify/future')
async def slashSpotifyFuture():
    return await spotifyFuture()

@app.route('/spotify/past')
async def slashSpotifyPast():
    return await spotifyPast()

@app.route('/spotify/callback')
async def slashSpotifyCallback():
    return await spotifyCallback(request)

@app.route('/spotify/now')
async def slashSpotifyNow():
    return await spotifyNow()

@app.route('/spotify/next')
async def slashSpotifyNext():
    return await spotifyNext()

@app.route('/spotify/previous')
async def slashSpotifyPrevious():
    return await spotifyPrevious()

# @app.route('/applemusic/past')
# async def slashAppleMusicPast():
#    return await appleMusicPast()

app.run(env['HOST'], port=int(env['PORT']))

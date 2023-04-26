import json
import os
from markupsafe import escape
from quart import Quart, request
from music.spotify.nowPlaying import nowPlaying as now
from music.spotify.queue import queue as queue
from music.spotify.history import history as history
from music.spotify.callback import callback as cb

app = Quart(__name__)


@app.route('/')
async def root():
    return ''


@app.route('/ping')
async def ping():
    return 441

@app.route('/spotify')
async def slashSpotify():
    return await now()
  
@app.route('/spotify/queue')
async def slashSpotifyQueue():
    return await queue()

@app.route('/spotify/history')
async def slashSpotifyHistory():
    return await history()

@app.route('/spotify/callback')
async def slashSpotifyCallback():
    return await cb(request)

app.run(host='0.0.0.0', port=8080)

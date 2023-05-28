import hashlib
import json
import os
from flask import Flask, request, Response

app = Flask(__name__)

# Get the list of shows
current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, "shows.txt")
with open(file_path, "r") as f:
    shows = [line.strip() for line in f.readlines()]


@app.route("/api")
def get_matching_shows():
    jsonp = False
    if "callback" in request.args:
        jsonp = True

    matching_shows = []
    if "q" in request.args:
        for show in shows:
            if request.args["q"] in show.lower():
                matching_shows.append(
                    {
                        "id": hashlib.md5(show.encode()).hexdigest(),
                        "name": show,
                    }
                )

    response_str = json.dumps(matching_shows)
    if jsonp:
        response_str = f"{request.args['callback']}({response_str})"

    resp = Response(response_str)
    if jsonp:
        resp.headers['Content-Type'] = 'application/javascript'
    else:
        resp.headers['Content-Type'] = 'application/json'

    return resp
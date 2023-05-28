import hashlib
import json
import os
from flask import Flask, request, Response, abort

app = Flask(__name__)

# Get the list of shows
current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, "shows.txt")
with open(file_path, "r") as f:
    shows = [line.strip() for line in f.readlines()]


# Create a JSON response, optionally wrapping it in a JSONP callback
def jsonify(data, jsonp_callback=False):
    response_str = json.dumps(data)
    if jsonp_callback:
        response_str = f"{jsonp_callback}({response_str})"

    resp = Response(response_str)
    if jsonp_callback:
        resp.headers["Content-Type"] = "application/javascript"
    else:
        resp.headers["Content-Type"] = "application/json"

    return resp


@app.route("/api")
def get_matching_shows():
    if "q" not in request.args:
        abort(400)

    matching_shows = []
    for show in shows:
        if request.args["q"] in show.lower():
            matching_shows.append(
                {
                    "id": hashlib.md5(show.encode()).hexdigest(),
                    "name": show,
                }
            )

    return jsonify(matching_shows, request.args.get("callback", False))

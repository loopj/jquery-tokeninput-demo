import hashlib
import json
import os
from flask import Flask, request

app = Flask(__name__)

# Get the list of shows
current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, "shows.txt")
with open(file_path, "r") as f:
    shows = [line.strip() for line in f.readlines()]


@app.route("/api")
def get_matching_shows():
    if "q" not in request.args:
        return json.dumps([])

    matching_shows = []
    for show in shows:
        if request.args["q"] in show.lower():
            matching_shows.append(
                {
                    "id": hashlib.md5(show.encode()).hexdigest(),
                    "name": show,
                }
            )

    return json.dumps(matching_shows)

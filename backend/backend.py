from typing import ItemsView
from flask import Flask, request
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

@app.route("/", methods=["POST"])
def hello_world():
    print(request.json)
    with open(f"{request.json['name']}-{request.json['timestamp']}", 'w') as f:
        json.dump(request.json, f)
        return ''

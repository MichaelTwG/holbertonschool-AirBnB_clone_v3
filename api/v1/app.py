#!/usr/bin/python3
"""
Endpoint (route) returns the status of an API
"""
from flask import Flask, jsonify
from models.__init__ import storage
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS

HBNB_API_HOST = getenv("HBNB_API_HOST")
HBNB_API_PORT = getenv("HBNB_API_PORT")

app = Flask(__name__)

CORS(app, origins='0.0.0.0')
app.url_map.strict_slashes = False


app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exit):
    """ Removes the current SQLAlchemy Session """
    storage.close()


@app.errorhandler(404)
def errorhandler404(e):
    """ Handles 404 error """
    print("asdasyyyyd")
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    if HBNB_API_HOST and HBNB_API_PORT:
        app.run(host=HBNB_API_HOST, debug=True,
                port=HBNB_API_PORT, threaded=True)
    else:
        app.run(host="0.0.0.0", debug=True, port=5000, threaded=True)

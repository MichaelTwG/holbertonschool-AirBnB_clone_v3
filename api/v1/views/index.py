#!/usr/bin/python3
""" Index file """
from api.v1.views.__init__ import app_views
from flask import jsonify


@app_views.route("/status")
def status():
    return jsonify({"status": "OK"})


@app_views.route("/stats")
def stats():
    from models.__init__ import storage

    return jsonify(
        {
            "amenities": storage.count("Amenity"),
            "cities": storage.count("City"),
            "places": storage.count("Place"),
            "reviews": storage.count("Review"),
            "states": storage.count("State"),
            "users": storage.count("User")
        }
    )

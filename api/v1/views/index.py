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
    from models.amenity import Amenity
    from models.city import City
    from models.place import Place
    from models.review import Review
    from models.state import State
    from models.user import User
    return jsonify(
        {
            "amenities": storage.count(Amenity),
            "cities": storage.count(City),
            "places": storage.count("Amenity"),
            "reviews": storage.count("Amenity"),
            "states": storage.count("Amenity"),
            "users": storage.count("Amenity")
        }
    )

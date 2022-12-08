#!/usr/bin/python3
""" cities file """
from api.v1.views.__init__ import app_views
from flask import jsonify, abort, request
from models.__init__ import storage
from models.city import City
from models.state import State


@app_views.route("/api/v1/cities/<city_id>/places", methods=["GET", "POST"])
def places_of_city(city_id):
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    if request.method == "GET":
        places = [place.to_dict() for place in city.places]
        return jsonify(places)

    if request.method == "POST":
        httpDict = request.get_json()
        if not httpDict or type(httpDict) != dict:
            abort(400, "Not a JSON")
        if "name" not in httpDict:
            abort(400, "Missing name")

        #httpDict["state_id"] = state_id
        newCity = City(**httpDict)
        newCity.save()
        return jsonify(newCity.to_dict()), 201


@app_views.route("/cities/<string:city_id>", methods=["GET", "DELETE"])
def get_city_by_id(city_id):
    obj = storage.get(City, city_id)
    if request.method == "GET":
        if obj is None:
            abort(404)
        return jsonify(obj.to_dict())
    elif request.method == "DELETE":
        if obj is None:
            abort(404)

        storage.delete(obj)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route("/cities/<string:city_id>", methods=["PUT"])
def put_city(city_id):
    obj = storage.get(City, city_id)
    if obj is None:
        abort(404)

    updated_dict = request.get_json()
    if updated_dict is None or type(updated_dict) != dict:
        abort(400, "Not a JSON")
    for key, value in updated_dict.items():
        if key not in ["id", "created_at", "updated_at", "state_id"]:
            setattr(obj, key, value)
    storage.save()
    return jsonify(obj.to_dict()), 200

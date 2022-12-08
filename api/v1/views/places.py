#!/usr/bin/python3
""" cities file """
from api.v1.views.__init__ import app_views
from flask import jsonify, abort, request
from models.__init__ import storage
from models.city import City
from models.state import State
from models.user import User
from models.place import Place

@app_views.route("/cities/<city_id>/places", methods=["GET", "POST"])
def places_of_city(city_id):
    cities_list = [obj.to_dict() for obj in storage.all("City").values()]
    ids = [obj['id'] for obj in cities_list]
    if city_id in ids:
        if request.method == "GET":
            cities = storage.all("Place")
            city_places = [obj.to_dict() for obj in cities.values()
                           if obj.city_id == city_id]
            return jsonify(city_places)
        elif request.method == "POST":
            req_json = request.get_json()
            if not req_json:
                abort(400, 'Not a JSON')
            if not req_json.get("user_id"):
                abort(400, "Missing user_id")
            user = storage.get(User, req_json.get("user_id"))
            if not user:
                abort(404, "Not found")
            if 'name' not in req_json:
                abort(400, 'Missing name')
            req_json["city_id"] = city_id
            new_place = Place(**req_json)
            new_place.save()
            return jsonify(new_place.to_dict()), 201
    else:
        abort(404)


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

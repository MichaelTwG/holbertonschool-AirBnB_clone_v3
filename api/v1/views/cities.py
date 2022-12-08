#!/usr/bin/python3
""" cities file """
from api.v1.views.__init__ import app_views
from flask import jsonify, abort, request
from models.__init__ import storage
from models.city import City
from models.state import State

@app_views.route("/states/<string:state_id>/cities")
def cities_of_states(state_id):
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    ci = []
    for st in state.cities:
        ci.append(st.to_dict())
    return jsonify(ci)


@app_views.route("/cities", methods=["POST"])
def get_Citys():
    if request.method == "POST":
        httpDict = request.get_json()
    if not httpDict:
        abort(400, "Not a JSON")
    if "name" not in httpDict:
        abort(400, "Missing name")
    if "state_id" not in httpDict:
        abort(404)
    else:
        state = storage.get(State, httpDict["state_id"])
        if state is None:
            raise(404)
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

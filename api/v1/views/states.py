#!/usr/bin/python3
""" states file """
from api.v1.views.__init__ import app_views
from flask import jsonify, abort, request
from models.__init__ import storage
from models.state import State


@app_views.route("/states", methods=["GET", "POST"])
def get_states():
    if request.method == "GET":
        return jsonify([obj.to_dict() for obj in storage.all("State").values()])
    elif request.method == "POST":
        httpDict = request.get_json()
    if not httpDict:
        abort(400, "Not a JSON")
    if "name" not in httpDict:
        abort(400, "Missing name")
    newState = State(**httpDict)
    newState.save()
    return jsonify(newState.to_dict()), 201


@app_views.route("/states/<string:state_id>", methods=["GET", "DELETE"])
def get_state_by_id(state_id):
    obj = storage.get(State, state_id)
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


@app_views.route("/states/<string:state_id>", methods=["PUT"])
def put_state(state_id):
    obj = storage.get(State, state_id)
    if obj is None:
        abort(404)

    updated_dict = request.get_json()
    if updated_dict is None or type(updated_dict) != dict:
        abort(400, "Not a JSON")
    for key, value in updated_dict.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(obj, key, value)
    storage.save()
    return jsonify(obj.to_dict()), 200

#!/usr/bin/python3
"""
Module places
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place


@app_views.route('/cities/<city_id>/places',
                 strict_slashes=False, methods=['GET'])
def places_by_cityid(city_id):
    for i in storage.all("City").values():
        if i.id == city_id:
            my_city = storage.all()["City" + '.' + city_id]
            my_list = []
            if my_city.places:
                for i in storage.all("Place").values():
                    if i.city_id == city_id:
                        my_list.append(i.to_dict())
            return jsonify(my_list)
    abort(404)


@app_views.route('/places/<place_id>', strict_slashes=False, methods=['GET'])
def get_places(place_id):
    for i in storage.all("Place").values():
        if i.id == place_id:
            my_place = storage.all()["Place" + '.' + place_id]
            return jsonify(my_place.to_dict())
    abort(404)


@app_views.route('/places/<place_id>',
                 strict_slashes=False, methods=['DELETE'])
def delete_places_byid(place_id):
    for i in storage.all("Place").values():
        if i.id == place_id:
            my_place = storage.all()["Place" + '.' + place_id]
            storage.delete(my_place)
            storage.save()
            return jsonify({})
    abort(404)


@app_views.route('/cities/<city_id>/places',
                 strict_slashes=False, methods=['POST'])
def create_places_byid(city_id):
    for i in storage.all("City").values():
        if i.id == city_id:
            npl = request.get_json(silent=True)
            if npl is None:
                abort(400, 'Not a JSON')
            if 'user_id' not in npl.keys():
                abort(400, 'Missing user_id')
            if 'name' not in npl.keys():
                abort(400, 'Missing name')
            tmp_list = []
            for i in storage.all("User").values():
                tmp_list.append(i.id)
            for key, value in npl.items():
                if key == 'user_id':
                    if value not in tmp_list:
                        abort(404)
            npl["city_id"] = city_id
            my_place = Place(**npl)
            storage.new(my_place)
            storage.save()
            return jsonify(my_place.to_dict()), 201
    abort(404)


@app_views.route('/places/<place_id>', strict_slashes=False, methods=['PUT'])
def update_place(place_id):
    upl = request.get_json(silent=True)
    if upl is None:
        abort(400, 'Not a JSON')
    for i in storage.all("Place").values():
        if i.id == place_id:
            my_place = storage.all()["Place" + '.' + place_id]
            for key, value in upl.items():
                if key == 'id' or key == 'created_at' \
                   or key == 'updated_at' or key == 'user_id' \
                   or key == 'city_id':
                    pass
                else:
                    setattr(my_place, key, value)
            storage.save()
            return jsonify(my_place.to_dict()), 200
    abort(404)

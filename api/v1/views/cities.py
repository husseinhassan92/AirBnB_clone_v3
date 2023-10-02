#!/usr/bin/python3
"""RESTful API for class City"""

from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.city import City


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def get_cities(state_id):
    """return city list by state id"""
    state = storage.get('State', state_id)
    if state is None:
        abort(404)

    list = []
    for city in state.cities:
        list.append(city.to_dict())
    return jsonify(list)


@app_views.route('/cities/<city_id>',
                 methods=['GET'], strict_slashes=False)
def get_city_id(city_id):
    """return city and its id using http verb GET"""
    city = storage.get('City', city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>',
                 methods=['DELETE'], strict_slashes=False)
def del_city(city_id):
    """delete the city"""
    city = storage.get('City', city_id)
    if city is None:
        abort(404)
    storage.delete()
    storage.save()

    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def create_city(state_id):
    """create new state obj"""
    if not request.get_json():
        return jsonify({'error', 'Not a JSON'}), 400
    elif 'name' not in request.get_json():
        return jsonify({"error": 'Missing name'}), 400
    else:
        obj = request.get_json()
        state = storage.get("State", state_id)
        if state is None:
            abort(404)

        obj['state_id'] = state.id
        city = City(**obj)
        city.save()
        return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>',
                 methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """update existing city object"""
    if not request.get_json():
        return jsonify({'error', 'Not a JSON'}), 400

    city = storage.get('City', city_id)
    if city is None:
        abort(404)
    obj_data = request.get_json()
    city.name = obj_data['name']
    city.save()
    return jsonify(city.to_dict()), 200

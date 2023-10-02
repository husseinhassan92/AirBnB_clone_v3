#!/usr/bin/python3
"""RESTful API for class State"""

from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def list_state():
    """return state in json form"""
    list = []
    for state in storage().all('State').values():
        list.append(state.to_dict())
    return jsonify(list)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def state_id(state_id):
    """return state and its id using http verb GET"""
    state = storage.get('State', state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>',
                 methods=['DELETE'], strict_slashes=False)
def del_state(state_id):
    """delete the state"""
    state = storage.get('State', state_id)
    if state is None:
        abort(404)
    storage.delete()
    storage.save()

    return jsonify({}), 200


@app_views.route('/states',
                 methods=['POST'], strict_slashes=False)
def create_state():
    """create new state obj"""
    if not request.get_json():
        return jsonify({'error', 'Not a JSON'}), 400
    elif 'name' not in request.get_json():
        return jsonify({"error": 'Missing name'}), 400
    else:
        obj = request.get_json()
        state = State(**obj)
        state.save()
        return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """update existing state object"""
    if not request.get_json():
        return jsonify({'error', 'Not a JSON'}), 400

    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    obj_data = request.get_json()
    state.name = obj_data['name']
    state.save()
    return jsonify(state.to_dict()), 200

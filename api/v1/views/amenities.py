#!/usr/bin/python3
"""RESTful API for class amenity"""

from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def list_amenitiy():
    """return amenity in json form"""
    list = []
    for amenity in storage().all('Amenity').values():
        list.append(amenity.to_dict())
    return jsonify(list)


@app_views.route('/amenities/<amenity_id>',
                 methods=['GET'], strict_slashes=False)
def amenity_id(amenity_id):
    """return amenity and its id using http verb GET"""
    amenity = storage.get('Amenity', amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def del_amenity(amenity_id):
    """delete the amenity"""
    amenity = storage.get('Amenity', amenity_id)
    if amenity is None:
        abort(404)
    storage.delete()
    storage.save()

    return jsonify({}), 200


@app_views.route('/amenities',
                 methods=['POST'], strict_slashes=False)
def create_amenity():
    """create new amenity obj"""
    if not request.get_json():
        return jsonify({'error', 'Not a JSON'}), 400
    elif 'name' not in request.get_json():
        return jsonify({"error": 'Missing name'}), 400
    else:
        obj = request.get_json()
        amenity = Amenity(**obj)
        amenity.save()
        return jsonify(amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>',
                 methods=['PUT'], strict_slashes=False)
def update_amenity(amenity_id):
    """update existing amenity object"""
    if not request.get_json():
        return jsonify({'error', 'Not a JSON'}), 400

    amenity = storage.get('Amenity', amenity_id)
    if amenity is None:
        abort(404)
    obj_data = request.get_json()
    amenity.name = obj_data['name']
    amenity.save()
    return jsonify(amenity.to_dict()), 200

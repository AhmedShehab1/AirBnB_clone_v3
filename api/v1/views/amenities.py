#!/usr/bin/python3
"""
New view for Amenity to handle default RestFul API actions
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity


def get_items(cls, id=None):
    items = storage.all(cls).values()
    if id is None:
        return items
    else:
        item = storage.get(cls, id)
        if item:
            return item
    abort(404)


def update_item(item, dict):
    for k, v in dict.items():
        if k in ['id', 'created_at', 'updated_at']:
            continue
        setattr(item, k, v)
    storage.save()


@app_views.route('/amenities', methods=['POST'])
def add_amenity():
    item_dict = request.get_json()
    if item_dict is None:
        return "Not a JSON", 400
    elif item_dict.get('name') is None:
        return 'Missing name', 400
    new_amenity = Amenity(**item_dict)
    new_amenity.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.get('/amenities/')
def all_amenity():
    return jsonify([amenity.to_dict() for amenity in get_items(Amenity)]), 200


@app_views.route('/amenities/<string:amenity_id>',
                 methods=['GET', 'DELETE', 'PUT'])
def amenity_by_id(amenity_id):
    amenity = get_items(Amenity, amenity_id)
    if request.method == 'GET':
        return jsonify(amenity.to_dict())
    elif request.method == 'PUT':
        to_add = request.get_json()
        if to_add is None:
            return 'Not a JSON', 400
        update_item(amenity, to_add)
        return jsonify(amenity.to_dict()), 200

    storage.delete(amenity)
    return {}, 200

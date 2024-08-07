#!/usr/bin/python3
"""
New view for Place to handle default RestFul API actions
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.city import City
from models.place import Place
from models.user import User


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
        if k in ['id', 'created_at', 'updated_at', 'user_id', 'city_id']:
            continue
        setattr(item, k, v)
    storage.save()


@app_views.route('/cities/<string:city_id>/places', methods=['GET', 'POST'])
def city_places(city_id):
    city = get_items(City, city_id)
    if request.method == 'GET':
        return jsonify([place.to_dict() for place in city.places])
    elif request.method == 'POST':
        data = request.get_json()
        if data is None:
            return "Not a JSON", 400
        elif data.get('user_id') is None:
            return 'Missing user_id', 400
        elif data.get('name') is None:
            return 'Missing name', 400
        user = get_items(User, data.get('user_id'))
        data.update({'city_id': city.id, 'user_id': user.id})
        new_place = Place(**data)
        new_place.save()
        return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<string:place_id>', methods=['GET', 'DELETE', 'PUT'])
def place_by_id(place_id):
    place = get_items(Place, place_id)
    if request.method == 'GET':
        return jsonify(place.to_dict())
    elif request.method == 'PUT':
        data = request.get_json()
        if data is None:
            return 'Not a JSON', 400
        update_item(place, data)
        return jsonify(place.to_dict()), 200

    storage.delete(place)
    return {}, 200

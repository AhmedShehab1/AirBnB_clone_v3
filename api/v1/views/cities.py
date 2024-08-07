#!/usr/bin/python3
"""
New view for City to handle default RestFul API actions
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State
from models.city import City


def get_items(cls, id=None):
    if id is None:
        return storage.all(cls).values()
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


@app_views.route('/states/<string:state_id>/cities', methods=['GET', 'POST'])
def cities_of_state(state_id):
    state = get_items(State, state_id)
    if request.method == 'GET':
        return jsonify([city.to_dict() for city in state.cities]), 200
    elif request.method == 'POST':
        item_dict = request.get_json()
        if item_dict is None:
            return "Not a JSON", 400
        elif item_dict.get('name') is None:
            return 'Missing name', 400
        item_dict.update({'state_id': state_id})
        new_city = City(**item_dict)
        new_city.save()
        return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<string:city_id>', methods=['GET', 'DELETE', 'PUT'])
def city_by_id(city_id):
    city = get_items(City, city_id)
    if request.method == 'GET':
        return jsonify(city.to_dict())
    elif request.method == 'PUT':
        to_add = request.get_json()
        if to_add is None:
            return 'Not a JSON', 400
        update_item(city, to_add)
        return jsonify(city.to_dict()), 200

    storage.delete(city)  # "Unknown column 'places.city_id' in 'field list'"
    return {}, 200

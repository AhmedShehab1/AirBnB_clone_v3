#!/usr/bin/python3
"""
New view for State to handle default RestFul API actions
"""
from api.v1.views import app_views
from models import storage
from models.state import State
from flask import abort, jsonify, request


def get_items(id=None):
    states = storage.all(State).values()
    if id is None:
        return states
    else:
        for state in states:
            if id == state.id:
                return state
    abort(404)


def update_item(item, dict):
    for k, v in dict.items():
        if k in ['id', 'created_at', 'updated_at']:
            continue
        setattr(item, k, v)
    storage.save()


@app_views.get('/states/')
def all_state():
    return jsonify([state.to_dict() for state in get_items()]), 200


@app_views.route('/states/<string:id>', methods=['GET', 'DELETE', 'PUT'])
def state(id):
    result = get_items(id)
    if request.method == 'GET':
        return jsonify(result.to_dict()), 200

    if request.method == 'PUT':
        data = request.get_json()
        if not data:
            return "Not a JSON", 400
        update_item(result, data)
        return jsonify(result.to_dict()), 200

    # else delete -------------------to be fixed---------------
    storage.delete(result)
    return {}, 200


@app_views.post('/states/')
def create_state():
    data = request.get_json()
    if not data:
        return "Not a JSON", 400
    if not data.get('name'):
        return "Missing name", 400
    new_state = State(**data)
    new_state.save()  # Not Being Saved to db,
# (After restarting the server it works)
    return jsonify(new_state.to_dict()), 201

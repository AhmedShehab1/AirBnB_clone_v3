#!/usr/bin/python3
"""
New view for User to handle default RestFul API actions
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
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
        if k in ['id', 'created_at', 'updated_at', 'email']:
            continue
        setattr(item, k, v)
    storage.save()


@app_views.route('/users', methods=['POST'])
def add_user():
    item_dict = request.get_json()
    if item_dict is None:
        return "Not a JSON", 400
    elif item_dict.get('email') is None:
        return 'Missing email', 400
    elif item_dict.get('password') is None:
        return 'Missing password', 400
    new_user = User(**item_dict)
    new_user.save()
    return jsonify(new_user.to_dict()), 201


@app_views.get('/users/')
def all_users():
    return jsonify([user.to_dict() for user in get_items(User)]), 200


@app_views.route('/users/<string:user_id>', methods=['GET', 'DELETE', 'PUT'])
def user_by_id(user_id):
    user = get_items(User, user_id)
    if request.method == 'GET':
        return jsonify(user.to_dict())
    elif request.method == 'PUT':
        to_add = request.get_json()
        if to_add is None:
            return 'Not a JSON', 400
        update_item(user, to_add)
        return jsonify(user.to_dict()), 200

    storage.delete(user)
    return {}, 200

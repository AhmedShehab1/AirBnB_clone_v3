#!/usr/bin/python3
"""
New view for Review to handle default RestFul API actions
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.review import Review
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
        if k in ['id', 'created_at', 'updated_at', 'user_id', 'place_id']:
            continue
        setattr(item, k, v)
    storage.save()


@app_views.route('/places/<string:place_id>/reviews', methods=['GET', 'POST'])
def place_reviews(place_id):
    place = get_items(Place, place_id)
    if request.method == 'GET':
        return jsonify([review.to_dict() for review in place.reviews])
    elif request.method == 'POST':
        data = request.get_json()
        if data is None:
            return "Not a JSON", 400
        elif data.get('user_id') is None:
            return 'Missing user_id', 400
        elif data.get('text') is None:
            return 'Missing text', 400
        user = get_items(User, data.get('user_id'))
        data.update({'place_id': place.id, 'user_id': user.id})
        new_review = Review(**data)
        new_review.save()
        return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<string:review_id>',
                 methods=['GET', 'DELETE', 'PUT'])
def review_by_id(review_id):
    review = get_items(Review, review_id)
    if request.method == 'GET':
        return jsonify(review.to_dict())
    elif request.method == 'PUT':
        data = request.get_json()
        if data is None:
            return 'Not a JSON', 400
        update_item(review, data)
        return jsonify(review.to_dict()), 200

    storage.delete(review)
    return {}, 200

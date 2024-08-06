#!/usr/bin/python3
"""
defining some routes
"""
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.user import User
from models.state import State

classes = {"amenities": Amenity, "cities": City,
           "places": Place, "reviews": Review, "states": State, "users": User}


@app_views.route('/status')
def status():
    return {'status': 'OK'}


@app_views.route('/stats')
def stats():
    count_dict = {}
    for k, v in classes.items():
        count_dict.update({k: storage.count(v)})
    return count_dict

#!/usr/bin/python3
"""Index fiile of the api"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route("/status", methods=['GET'], strict_slashes=False)
def status():
    """get status"""
    return jsonify(status='OK')


@app_views.route("/stats",
                 methods=['GET'], strict_slashes=False)
def count():
    classes = {"amenities": "Amenity",
               "cities": "City",
               "places": "Place",
               "reviews": "Review",
               "states": "State",
               "users": "User"}
    for k, v in classes.items():
        classes[k] = storage.count(v)
    return classes

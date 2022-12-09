#!/usr/bin/python3
"""Index file of the api"""
from api.v1.views import app_views
from models import storage
from flask import abort, request, jsonify
from models.amenity import Amenity
import json


@app_views.route("/amenities", methods=['GET'],
                 strict_slashes=False)
def amenities():
    """Retrieves the list of all Amenity objects"""
    list_obj = []
    amenity = storage.all(Amenity).values()
    for v in amenities:
        list_obj.append(v.to_dict())
    return jsonify(list_obj)


@app_views.route("/amenities", methods=['POST'],
                 strict_slashes=False)
def post_amenity():
    """Creates a Amenity"""

    d = request.get_json(silent=True)
    if d is None:
        abort(400, description="Not a JSON")
    elif "name" not in d.keys():
        abort(400, description="Missing name")
    obj = Amenity(**d)
    obj.save()
    return obj.to_dict(), 201


@app_views.route("/amenities/<amenity_id>", methods=['GET'],
                 strict_slashes=False)
def get_amenity_object(amenity_id):
    """Retrieves a Amenity object"""
    obj = storage.get(Amenity, amenity_id)
    if obj:
        return jsonify(obj.to_dict())
    else:
        abort(404)


@app_views.route("/amenities/<amenity_id>", methods=['DELETE'],
                 strict_slashes=False)
def del_city_object(amenity_id):
    """Deletes a Amenity object"""
    obj = storage.get(Amenity, amenity_id)
    if obj:
        storage.delete(obj)
        storage.save()
        return {}
    else:
        abort(404)


@app_views.route("/amenities/<amenity_id>", methods=['PUT'],
                 strict_slashes=False)
def put_city_object(amenity_id):
    """Updates a City object"""
    obj = storage.get(Amenity, amenity_id)
    d = request.get_json(silent=True)
    if not obj:
        abort(404)
    if d is None:
        abort(400, description="Not a JSON")

    for k, v in d.items():
        if k != "id" and k != "created_at" and k != "updated_at":
            setattr(obj, k, v)
    storage.save()
    return obj.to_dict()

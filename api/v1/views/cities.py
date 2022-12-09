#!/usr/bin/python3
"""Index file of the api"""
from api.v1.views import app_views
from models import storage
from flask import abort, request, jsonify
from models.state import State
from models.city import City
import json


@app_views.route("/states/<state_id>/cities", methods=['GET'],
                 strict_slashes=False)
def cities(state_id):
    """Retrieves the list of all City objects of a State"""
    list_obj = []
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    for v in state.cities:
        list_obj.append(v.to_dict())
    return jsonify(list_obj)


@app_views.route("/states/<state_id>/cities", methods=['POST'],
                 strict_slashes=False)
def post_city(state_id):
    """Creates a City"""
    state = storage.get(State, state_id)
    d = request.get_json(silent=True)
    if not state:
        abort(404)
    if d is None:
        abort(400, description="Not a JSON")
    elif "name" not in d.keys():
        abort(400, description="Missing name")
    obj = City(**d)
    obj.save()
    obj.state_id = state.id
    return jsonify(obj.to_dict()), 201


@app_views.route("/cities/<city_id>", methods=['GET'],
                 strict_slashes=False)
def get_city_object(city_id):
    """Retrieves a City object"""
    obj = storage.get(City, city_id)
    if obj:
        return jsonify(obj.to_dict())
    else:
        abort(404)


@app_views.route("/cities/<city_id>", methods=['DELETE'],
                 strict_slashes=False)
def del_city_object(city_id):
    """Deletes a City object"""
    obj = storage.get(City, city_id)
    if obj:
        storage.delete(obj)
        storage.save()
        return {}
    else:
        abort(404)


@app_views.route("/cities/<city_id>", methods=['PUT'],
                 strict_slashes=False)
def put_city_object(city_id):
    """Updates a City object"""
    obj = storage.get(City, city_id)
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

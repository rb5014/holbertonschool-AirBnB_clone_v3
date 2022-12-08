#!/usr/bin/python3
"""Index file of the api"""
from api.v1.views import app_views
from models import storage
from flask import abort, request, jsonify
from models.state import State
import json


@app_views.route("/states", methods=['GET'],
                 strict_slashes=False)
def states():
    """Retrieves the list of all State objetcs"""
    list_obj = []
    for k, v in storage.all(State).items():
        list_obj.append(v.to_dict())
    return json.dumps(list_obj, indent=4)


@app_views.route("/states", methods=['POST'],
                 strict_slashes=False)
def post_states():
    """Creates a state"""
    d = request.get_json(silent=True)
    if d is None:
        abort(400, description="Not a JSON")
    elif "name" not in d.keys():
        abort(400, description="Missing name")
    return jsonify(State(d).to_dict, status=201)


@app_views.route("/states/<state_id>", methods=['GET'],
                 strict_slashes=False)
def get_state_object(id):
    """Retrieves a State object"""
    obj = storage.get(State, id)
    if obj:
        return json.dumps(obj.to_dict(), indent=4)
    else:
        abort(404, description="Resource not found")


@app_views.route("/states/<state_id>", methods=['DELETE'],
                 strict_slashes=False)
def del_state_object(id):
    """Deletes a State object"""
    obj = storage.get(State, id)
    if obj:
        storage.delete(obj)
        return {}
    else:
        abort(404, description="Resource not found")


@app_views.route("/api/v1/states/<state_id>", methods=['PUT'],
                 strict_slashes=False)
def put_state_object():
    """Updates a State object"""
    obj = storage.get("State", id)
    d = request.get_json(silent=True)
    if d is None:
        abort(400, description="Not a JSON")

    for k, v in d.items():
        if k != "id" and k != "created_at" and k != "updated_at":
            setattr(obj, k, v)
    return obj

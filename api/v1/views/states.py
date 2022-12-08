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
    obj = State(**d)
    obj.save()
    return json.dumps(obj.to_dict(), indent=4), 201


@app_views.route("/states/<state_id>", methods=['GET'],
                 strict_slashes=False)
def get_state_object(state_id):
    """Retrieves a State object"""
    obj = storage.get(State, state_id)
    if obj:
        return json.dumps(obj.to_dict(), indent=4)
    else:
        abort(404)


@app_views.route("/states/<state_id>", methods=['DELETE'],
                 strict_slashes=False)
def del_state_object(state_id):
    """Deletes a State object"""
    obj = storage.get(State, state_id)
    if obj:
        storage.delete(obj)
        storage.save()
        return {}
    else:
        abort(404)


@app_views.route("/states/<state_id>", methods=['PUT'],
                 strict_slashes=False)
def put_state_object(state_id):
    """Updates a State object"""
    obj = storage.get(State, state_id)
    d = request.get_json(silent=True)
    if d is None:
        abort(400, description="Not a JSON")

    for k, v in d.items():
        if k != "id" and k != "created_at" and k != "updated_at":
            setattr(obj, k, v)
    return json.dumps(obj.to_dict(), indent=4)

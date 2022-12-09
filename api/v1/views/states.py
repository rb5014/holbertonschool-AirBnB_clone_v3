#!/usr/bin/python3
"""RESTful API actions for State objects"""
from flask import abort, request, jsonify
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route("/states", methods=['GET'],
                 strict_slashes=False)
def states():
    """Retrieves the list of all State objetcs"""
    list_obj = []
    for obj in storage.all(State).values():
        list_obj.append(obj.to_dict())
    return jsonify(list_obj)


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
    return jsonify(obj.to_dict()), 201


@app_views.route("/states/<state_id>", methods=['GET'],
                 strict_slashes=False)
def get_state_object(state_id):
    """Retrieves a State object"""
    obj = storage.get(State, state_id)
    if obj:
        return jsonify(obj.to_dict())
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
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route("/states/<state_id>", methods=['PUT'],
                 strict_slashes=False)
def put_state_object(state_id):
    """Updates a State object"""
    d = request.get_json(silent=True)
    if d is None:
        abort(400, description="Not a JSON")

    obj = storage.get(State, state_id)
    if obj is None:
        abort(404)
    for k, v in d.items():
        if k != "id" and k != "created_at" and k != "updated_at":
            setattr(obj, k, v)
    storage.save()
    return jsonify(obj.to_dict())

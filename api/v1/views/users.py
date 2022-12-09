#!/usr/bin/python3
"""Index file of the api"""
from flask import abort, request, jsonify
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route("/users", methods=['GET'],
                 strict_slashes=False)
def users():
    """Retrieves the list of all users objetcs"""
    list_obj = []
    for k, v in storage.all(User).items():
        list_obj.append(v.to_dict())
    return jsonify(list_obj)


@app_views.route("/users", methods=['POST'],
                 strict_slashes=False)
def post_users():
    """Creates a users"""
    d = request.get_json(silent=True)
    if d is None:
        abort(400, description="Not a JSON")
    elif "name" not in d.keys():
        abort(400, description="Missing name")
    obj = User(**d)
    obj.save()
    return jsonify(obj.to_dict()), 201


@app_views.route("/users/<user_id>", methods=['GET'],
                 strict_slashes=False)
def get_user_object(user_id):
    """Retrieves a State object"""
    if user_id is None:
        abort(404)
    else:
        obj = storage.get(User, user_id)
        if obj:
            return jsonify(obj.to_dict())
        else:
            abort(404)


@app_views.route("/users/<user_id>", methods=['DELETE'],
                 strict_slashes=False)
def del_user_object(user_id):
    """Deletes a State object"""
    obj = storage.get(User, user_id)
    if obj:
        storage.delete(obj)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route("/users/<user_id>", methods=['PUT'],
                 strict_slashes=False)
def put_user_object(user_id):
    """Updates a user object"""
    d = request.get_json(silent=True)
    if d is None:
        abort(400, description="Not a JSON")

    obj = storage.get(User, user_id)
    ignore_key = ["id", "email", "created_at", "updated_at"]
    if obj is None:
        abort(404)
    for k, v in d.items():
        if k not in ignore_key:
            setattr(obj, k, v)
    storage.save()
    return jsonify(obj.to_dict())

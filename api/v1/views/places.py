#!/usr/bin/python3
"""RESTFULL API for State object view """
from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route("/cities/<city_id>/places", strict_slashes=False,
                 methods=['GET'])
def places(city_id):
    """retrieve place object(s)"""
    c_list = []

    if city_id is not None:

        city = storage.get(City, city_id)

        if city is None:
            abort(404)

        places = storage.all(Place)

        for v in places.values():
            if getattr(v, 'city_id') == city_id:
                c_list.append(v.to_dict())

        return jsonify(c_list)

    else:
        abort(404)


@app_views.route("/cities/<city_id>/places", strict_slashes=False,
                 methods=['POST'])
def post_place(city_id):
    """Adds a place object"""
    data = request.get_json()

    if data is None:
        abort(400, description="Not a JSON")

    if "user_id" not in data:
        abort(400, description="Missing user_id")

    if "name" not in data:
        abort(400, description="Missing name")

    if city_id is not None:

        user = storage.get(User, data["user_id"])

        city = storage.get(City, city_id)

        if user is None:
            abort(404)

        if city is None:
            abort(404)

        obj = Place(**data)

        setattr(obj, 'city_id', city_id)
        obj.save()
        return jsonify(obj.to_dict()), 201

    else:
        abort(404)


@app_views.route("/places/<place_id>", strict_slashes=False,
                 methods=['GET'])
def get_place_object(place_id):
    """Retreive place object with place_id"""
    if place_id is not None:

        place = storage.get(Place, place_id)

        if place is None:
            abort(404)

        return jsonify(place.to_dict())

    else:
        abort(404)


@app_views.route("/places/<place_id>", strict_slashes=False,
                 methods=['DELETE'])
def place_delete(place_id):
    """Deletes a place object """
    if place_id is not None:
        place = storage.get(Place, place_id)

        if place is None:
            abort(404)

        place.delete()
        storage.save()
        return jsonify({}), 200

    else:
        abort(404)


@app_views.route("/places/<place_id>", strict_slashes=False, methods=['PUT'])
def place_update(place_id):
    """Update a place object"""
    data = request.get_json(silent=True)

    if data is None:
        abort(400, description="Not a JSON")

    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    ignore_key = ["id", "user_id", "city_id", "created_at", "updated_at"]
    for k, v in place.items():
        if k not in ignore_key:
            setattr(place, k, v)
    storage.save()
    return jsonify(place.to_dict()), 200

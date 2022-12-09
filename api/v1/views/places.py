#!/usr/bin/python3
"""State object view """
from flask import abort, jsonify, request
from models.state import State
from models.city import City
from models.place import Place
from models import storage
from api.v1.views import app_views


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

        for k, v in places.items():
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

        user = storage.get("User", data["user_id"])

        city = storage.get("City", city_id)

        if user is None:
            abort(404)

        if city is None:
            abort(404)

        obj = Place(**data)

        setattr(obj, 'city_id', city_id)
        storage.new(obj)
        storage.save()
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
        place = storage.get("Place", place_id)

        if place is None:
            abort(404)

        place.delete()
        storage.save()
        return {}

    else:
        abort(404)


@app_views.route("/places/<place_id>", strict_slashes=False, methods=['PUT'])
def place_update(place_id):
    """Update a place object"""
    data = request.get_json()

    if data is None:
        abort(400, description="Not a JSON")

    place = storage.get("Place", place_id)

    if place is None:
        abort(404)

    if 'description' in data:
        setattr(place, 'description', data['description'])

    if 'number_rooms' in data:
        setattr(place, 'number_rooms', data['number_rooms'])

    if 'number_bathrooms' in data:
        setattr(place, 'number_bathrooms', data['number_bathrooms'])

    if 'max_guest' in data:
        setattr(place, 'max_guest', data['max_guest'])

    if 'price_by_night' in data:
        setattr(place, 'price_by_night', data['price_by_night'])

    if 'latitude' in data:
        setattr(place, 'latitude', data['latitude'])

    if 'longitude' in data:
        setattr(place, 'longitude', data['longitude'])

    if 'amenity_ids' in data:
        setattr(place, 'amenity_ids', data['amenity_ids'])

    setattr(place, 'name', data['name'])
    place.save()
    storage.save()

    return jsonify(place.to_dict())

#!/usr/bin/python3
"""RESTFULL API for State object view """
from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.user import User
from models.review import Review


@app_views.route("/places/<place_id>/reviews", strict_slashes=False,
                 methods=['GET'])
def reviews(place_id):
    """retrieve reviews object(s)"""
    r_list = []

    place = storage.get(Place, place_id)

    if place is None:
        abort(404)

    reviews = storage.all(Review)

    for obj in reviews.values():
        if obj.place_id == place_id:
            r_list.append(obj.to_dict())
       
    return jsonify(r_list)


@app_views.route("/places/<place_id>/reviews", strict_slashes=False,
                 methods=['POST'])
def post_review(place_id):
    """Adds a place object"""
    data = request.get_json(silent=True)

    if data is None:
        abort(400, description="Not a JSON")

    if "user_id" not in data:
        abort(400, description="Missing user_id")

    if "text" not in data:
        abort(400, description="Missing text")

    if place_id is not None:

        user = storage.get(User, data["user_id"])

        place = storage.get(Place, place_id)

        if user is None:
            abort(404)

        if place is None:
            abort(404)

        data['place_id'] = place_id
        obj = Review(**data)

        obj.save()
        return jsonify(obj.to_dict()), 201

    else:
        abort(404)


@app_views.route("/reviews/<review_id>", strict_slashes=False,
                 methods=['GET'])
def get_review_object(review_id):
    """Retreive review object with review_id"""

    review = storage.get(Review, review_id)

    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route("reviews/<review_id>", strict_slashes=False,
                 methods=['DELETE'])
def review_delete(review_id):
    """Deletes a place object """
    if review_id is not None:
        review = storage.get(Review, review_id)

        if review is None:
            abort(404)

        storage.delete(review)
        storage.save()
        return jsonify({}), 200

    else:
        abort(404)


@app_views.route("/reviews/<review_id>", strict_slashes=False, methods=['PUT'])
def review_update(review_id):
    """Update a place object"""
    data = request.get_json(silent=True)

    if data is None:
        abort(400, description="Not a JSON")

    review = storage.get(Review, review_id)

    if not review:
        abort(404)

    ignore_key = ["id", "user_id", "place_id", "created_at", "updated_at"]
    for k, v in data.items():
        if k not in ignore_key:
            setattr(review, k, v)
    storage.save()
    return jsonify(review.to_dict()), 200

#!/usr/bin/python3
"""This module allows view for Review objects that handles
all default RESTFul API actions"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.review import Review
from models.place import Place
from models.user import User


@app_views.route('/places/<string:place_id>/reviews', methods=['GET', 'POST'],
                 strict_slashes=False)
def place_reviews(place_id):
    """
    Retrieves the list of all Review objects of a Place.
    Creates a Review for a Place.

    Raises:
        404: If no Place with the given ID exists.
        400: If the request body is not valid JSON or missing required fields.
    """
    if request.method == 'GET':
        place = storage.get(Place, place_id)
        if not place:
            abort(404)
        reviews = storage.all(Review)
        reviews_dict = [value.to_dict() for value in reviews.values()
                        if value.place_id == place_id]
        return jsonify(reviews_dict)
    elif request.method == 'POST':
        place = storage.get(Place, place_id)
        if not place:
            abort(404)
        json_data = request.get_json()
        if not json_data:
            abort(400, 'Not a JSON')
        required_fields = ['user_id', 'text']
        for field in required_fields:
            if field not in json_data:
                abort(400, f'Missing {field}')
        user_id = json_data['user_id']
        if not storage.get(User, user_id):
            abort(404)
        json_data['place_id'] = place_id
        new_review = Review(**json_data)
        new_review.save()
        return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<string:review_id>',
                 methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def review(review_id):
    """
    Retrieves a Review object.
    Deletes a Review object.
    Updates a Review object.

    Raises:
        404: If no Review with the given ID exists.
        400: If the request body is not valid JSON or improper fields
        attempted to be updated.
    """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    if request.method == 'GET':
        return jsonify(review.to_dict())
    elif request.method == 'DELETE':
        storage.delete(review)
        storage.save()
        return {}, 200
    elif request.method == 'PUT':
        json_data = request.get_json()
        if not json_data:
            abort(400, 'Not a JSON')
        for key, value in json_data.items():
            if key not in ['id', 'user_id', 'place_id',
                           'created_at', 'updated_at']:
                setattr(review, key, value)
        review.save()
        return jsonify(review.to_dict()), 200

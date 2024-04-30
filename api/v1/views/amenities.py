#!/usr/bin/python3
"""This module allows view for Amenity objects that handles
all default RESTFul API actions"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET', 'POST'], strict_slashes=False)
def amenities():
    """
    GET: Returns all amenities.
    POST: Creates an amenity.

    Raises:
        400: If the request body is not valid JSON or the 'name' key
        is missing.
    """
    if request.method == 'GET':
        amenities = [amenity.to_dict()
                     for amenity in storage.all(Amenity).values()]
        return jsonify(amenities)
    elif request.method == 'POST':
        json_data = request.get_json()
        if not json_data:
            abort(400, 'Not a JSON')
        if 'name' not in json_data:
            abort(400, 'Missing name')
        new_amenity = Amenity(**json_data)
        new_amenity.save()
        return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<string:amenity_id>',
                 methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def amenity(amenity_id):
    """
    Handles GET, DELETE, and PUT requests for a specific amenity by amenity_id
    GET: Returns the Amenity instance as JSON.
    DELETE: Deletes the Amenity instance.
    PUT: Updates the Amenity instance with provided JSON request body.

    Raises:
        404: If no Amenity with the given ID exists.
        400: If the request body is not valid JSON or improper fields
        attempted to be updated.
    """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    if request.method == 'GET':
        return jsonify(amenity.to_dict())
    elif request.method == 'DELETE':
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200
    elif request.method == 'PUT':
        json_data = request.get_json()
        if not json_data:
            abort(400, 'Not a JSON')
        for key, value in json_data.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(amenity, key, value)
        amenity.save()
        return jsonify(amenity.to_dict()), 200

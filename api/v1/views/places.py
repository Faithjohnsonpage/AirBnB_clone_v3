#!/usr/bin/python3
"""This module allows view for Place objects that handles
all default RESTFul API actions"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.city import City
from models.place import Place
from models.base_model import BaseModel
from models.user import User


@app_views.route('/cities/<string:city_id>/places', methods=['GET', 'POST'],
                 strict_slashes=False)
def places(city_id):
    """
    GET: Returns all places for a given city.
    POST: Creates a place under the given city.

    Raises:
        404: If no city with the given ID exists.
        400: If the request body is not valid JSON or missing required fields.
    """
    if request.method == 'GET':
        city = storage.get(City, city_id)
        if not city:
            abort(404)
        places = storage.all(Place)
        places_dict = [value.to_dict() for value in places.values()
                       if value.city_id == city_id]
        return jsonify(places_dict)
    elif request.method == 'POST':
        city = storage.get(City, city_id)
        if not city:
            abort(404)
        json_data = request.get_json()
        if not json_data:
            abort(400, 'Not a JSON')
        required_fields = ['user_id', 'name']
        for field in required_fields:
            if field not in json_data:
                abort(400, f'Missing {field}')
        user_id = json_data['user_id']
        if not storage.get(User, user_id):
            abort(404)
        new_place = Place(city_id=city_id, **json_data)
        new_place.save()
        return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<string:place_id>',
                 methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def place(place_id):
    """
    Handles GET, DELETE, and PUT requests for a specific place by place_id.
    GET: Returns the Place instance as JSON.
    DELETE: Deletes the Place instance.
    PUT: Updates the Place instance with provided JSON request body.

    Raises:
        404: If no Place with the given ID exists.
        400: If the request body is not valid JSON or improper fields
        attempted to be updated.
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if request.method == 'GET':
        return jsonify(place.to_dict())
    elif request.method == 'DELETE':
        storage.delete(place)
        storage.save()
        return {}, 200
    elif request.method == 'PUT':
        json_data = request.get_json()
        if not json_data:
            abort(400, 'Not a JSON')
        for key, value in json_data.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(place, key, value)
        place.save()
        return jsonify(place.to_dict()), 200

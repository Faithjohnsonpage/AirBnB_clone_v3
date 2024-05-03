#!/usr/bin/python3
"""This module allows view for State and City objects that handles
all default RESTFul API actions"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State
from models.city import City
from models.base_model import BaseModel


@app_views.route('/states/<string:state_id>/cities', methods=['GET', 'POST'],
                 strict_slashes=False)
def view_create_cities(state_id):
    """
    GET: Returns all cities for a given state.
    POST: Creates a city under the given state.

    Raises:
        404: If no state with the given ID exists or no cities found.
        400: If the request body is not valid JSON or the 'name' key
        is missing.
    """
    if request.method == 'GET':
        cities = []
        city_objs = storage.all(City)
        for city in city_objs.values():
            if city.state_id == state_id:
                cities.append(city)
        if not cities:
            abort(404)
        cities_dicts = [city.to_dict() for city in cities]
        return jsonify(cities_dicts)
    elif request.method == 'POST':
        state = storage.get(State, state_id)
        if not state:
            abort(404)
        json_data = request.get_json()
        if not json_data:
            abort(400, 'Not a JSON')
        if 'name' not in json_data:
            abort(400, 'Missing name')
        json_data['state_id'] = state_id
        new_city = City(**json_data)
        new_city.save()
        return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<string:city_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def view_update_delete_city(city_id):
    """
    Handles GET, DELETE, and PUT requests for a specific city by city_id.
    GET: Returns the City instance as JSON.
    DELETE: Deletes the City instance.
    PUT: Updates the City instance with provided JSON request body.

    Raises:
        404: If no City with the given ID exists.
        400: If the request body is not valid JSON or improper fields
        attempted to be updated.
    """
    if request.method == 'GET':
        city_objs = storage.all(City)
        for city in city_objs.values():
            if city.id == city_id:
                return jsonify(city.to_dict())
        abort(404)
    elif request.method == 'DELETE':
        city = storage.get(City, city_id)
        if not city:
            abort(404)
        storage.delete(city)
        storage.save()
        return jsonify({}), 200
    elif request.method == 'PUT':
        city = storage.get(City, city_id)
        if not city:
            abort(404)
        json_data = request.get_json()
        if not json_data:
            abort(400, 'Not a JSON')
        for key, value in json_data.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(city, key, value)
        storage.save()
        return jsonify(city.to_dict()), 200

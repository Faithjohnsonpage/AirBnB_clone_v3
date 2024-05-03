#!/usr/bin/python3
"""This module allows view for State objects that handles
all default RESTFul API actions"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State
from models.base_model import BaseModel


@app_views.route('/states', methods=['GET', 'POST'], strict_slashes=False)
def view_states():
    """
    Handle GET and POST requests for states endpoint.
    GET - Returns a list of all State instances as JSON.
    POST - Creates a new State instance from the JSON request body.
           Returns the new State instance as JSON with status code 201
           if successful.

    Raises:
        400: If the request body is not valid JSON or missing the 'name' key.
    """
    if request.method == 'GET':
        state_objs = storage.all(State)
        state_dicts = [state.to_dict() for state in state_objs.values()]
        return jsonify(state_dicts)
    elif request.method == 'POST':
        json_data = request.get_json()
        if not json_data:
            abort(400, 'Not a JSON')
        if 'name' not in json_data:
            abort(400, 'Missing name')
        new_state = State(**json_data)
        new_state.save()
        return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<string:state_id>', methods=['GET', 'PUT'],
                 strict_slashes=False)
def view_state(state_id):
    """
    Handle GET and PUT requests for a specific state by state_id.
    GET - Returns the State instance identified by state_id as JSON.
    PUT - Updates the State instance identified by state_id with
          the provided JSON request body.
          Returns the updated State instance as JSON with status
          code 200 if successful.

    Raises:
        400: If the request body is not valid JSON.
        404: If no State instance with the given state_id exists.
    """
    if request.method == 'GET':
        state_objs = storage.all(State)
        for state in state_objs.values():
            if state.id == state_id:
                return jsonify(state.to_dict())
        abort(404)
    elif request.method == 'PUT':
        state = storage.get(State, state_id)
        if not state:
            abort(404)
        json_data = request.get_json()
        if not json_data:
            abort(400, 'Not a JSON')
        for key, value in json_data.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(state, key, value)
        storage.save()
        return jsonify(state.to_dict()), 200


@app_views.route('/states/<string:state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """
    Handle DELETE requests for a specific state by state_id.
    Deletes the State instance and returns an empty dictionary with
    status code 200 if successful.

    Raises:
        404: If no State instance with the given state_id can be found.
    """
    state_objs = storage.all(State)
    for key, value in state_objs.items():
        if value.id == state_id:
            state_instance = value
            storage.delete(state_instance)
            storage.save()
            return jsonify({}), 200
    abort(404)

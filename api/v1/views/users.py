#!/usr/bin/python3
"""This module allows view for User objects that handles
all default RESTFul API actions"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET', 'POST'], strict_slashes=False)
def users():
    """
    GET: Returns all users.
    POST: Creates a user.

    Raises:
        400: If the request body is not valid JSON or the 'email'
        key is missing.
    """
    if request.method == 'GET':
        users = [user.to_dict() for user in storage.all(User).values()]
        return jsonify(users)
    elif request.method == 'POST':
        json_data = request.get_json()
        if not json_data:
            abort(400, 'Not a JSON')
        if 'email' not in json_data:
            abort(400, 'Missing email')
        if 'password' not in json_data:
            abort(400, 'Missing password')
        new_user = User(**json_data)
        new_user.save()
        return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<string:user_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def user(user_id):
    """
    Handles GET, DELETE, and PUT requests for a specific user by user_id.
    GET: Returns the User instance as JSON.
    DELETE: Deletes the User instance.
    PUT: Updates the User instance with provided JSON request body.

    Raises:
        404: If no User with the given ID exists.
        400: If the request body is not valid JSON or improper fields
        attempted to be updated.
    """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    if request.method == 'GET':
        return jsonify(user.to_dict())
    elif request.method == 'DELETE':
        storage.delete(user)
        storage.save()
        return jsonify({}), 200
    elif request.method == 'PUT':
        json_data = request.get_json()
        if not json_data:
            abort(400, 'Not a JSON')
        for key, value in json_data.items():
            if key not in ['id', 'email', 'created_at', 'updated_at']:
                setattr(user, key, value)
        user.save()
        return jsonify(user.to_dict()), 200

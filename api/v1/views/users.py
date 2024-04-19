#!/usr/bin/python3
"""Users view for API v1"""

from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_all_users():
    """Returns all User objects"""
    users = storage.all(User)
    users = [user.to_dict() for user in users.values()]
    return jsonify(users)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """Returns a User object"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """Deletes a User object"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """Creates a User object"""
    new_dict = request.get_json()
    if new_dict is None:
        return jsonify({"error": "Not a JSON"}), 400
    if 'email' not in new_dict:
        return jsonify({"error": "Missing email"}), 400
    if 'password' not in new_dict:
        return jsonify({"error": "Missing password"}), 400
    user = User(**new_dict)
    user.save()
    return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """Updates a User object"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    new_dict = request.get_json()
    if new_dict is None:
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in new_dict.items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, key, value)
    user.save()
    return jsonify(user.to_dict())

#!/usr/bin/python3
"""Places view for API v1"""

from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_all_places(city_id):
    """Returns all Place objects"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """Returns a Place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """Deletes a Place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """Creates a Place object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404) 
    if not request.is_json:
        return jsonify({"error": "Not a JSON"}), 400
    new_dict = request.get_json()
    if 'user_id' not in new_dict:
        return jsonify({"error": "Missing user_id"}), 400
    if 'name' not in new_dict:
        return jsonify({"error": "Missing name"}), 400
    user = storage.get(User, new_dict['user_id'])
    if user is None:
        abort(404)
    new_dict['city_id'] = city_id
    place = Place(**new_dict)
    place.save()
    return jsonify(place.to_dict()), 201

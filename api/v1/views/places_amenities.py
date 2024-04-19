#!/usr/bin/python3
"""Places amenities API"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.amenity import Amenity


@app_views.route('/places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def get_place_amenities(place_id):
    """Retrieves the list of all Amenity objects of a Place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if storage.__class__.__name__ == "DBStorage":
        amenities = [amenity.to_dict() for amenity in place.amenities]
    elif storage.__class__.__name__ == "FileStorage":
        amenities = [storage.get(Amenity, amenity_id).to_dict() for amenity_id
                     in place.amenity_ids]
    return jsonify(amenities)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_place_amenity(place_id, amenity_id):
    """Deletes an Amenity object to a Place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if storage.__class__.__name__ == "DBStorage":
        amenity = storage.get(Amenity, amenity_id)
        if amenity is None:
            abort(404)
        if amenity not in place.amenities:
            abort(404)
        place.amenities.delete(amenity)
    elif storage.__class.__name__ == "FileStorage":
        if amenity_id not in place.amenity_ids:
            abort(404)
        place.amenity_ids.remove(amenity_id)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['POST'],
                 strict_slashes=False)
def link_place_amenity(place_id, amenity_id):
    """Links an Amenity object to a Place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if storage.__class__.__name__ == "DBStorage":
        if amenity in place.amenities:
            return jsonify(amenity.to_dict()), 200
        place.amenities.append(amenity)
    elif storage.__class__.__name__ == "FileStorage":
        if amenity_id in place.amenity_ids:
            return jsonify(amenity.to_dict()), 200
        place.amenity_ids.append(amenity_id)
    storage.save()
    return jsonify(amenity.to_dict()), 201

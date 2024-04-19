#!/usr/bin/python3
"""Reviews view for API v1"""

from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.review import Review
from models.place import Place
from models.user import User


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_all_reviews(place_id):
    """Returns all Review objects"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """Returns a Review object"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """Deletes a Review object"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """Creates a Review object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    new_dict = request.get_json()
    if new_dict is None:
        return jsonify({"error": "Not a JSON"}), 400
    if 'user_id' not in new_dict:
        return jsonify({"error": "Missing user_id"}), 400
    if 'text' not in new_dict:
        return jsonify({"error": "Missing text"}), 400
    user = storage.get(User, new_dict['user_id'])
    if user is None:
        abort(404)
    new_dict['place_id'] = place_id
    review = Review(**new_dict)
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """Updates a Review object"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    new_dict = request.get_json()
    if new_dict is None:
        return jsonify({"error": "Not a JSON"}), 400
    for k, value in new_dict.items():
        if k not in ['id', 'user_id', 'place_id', 'created_at', 'updated_at']:
            setattr(review, k, value)
    review.save()
    return jsonify(review.to_dict()), 200

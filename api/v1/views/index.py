#!/usr/bin/python3
"""Index view for API v1"""

from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', strict_slashes=False)
def status():
    """Returns status"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False)
def stats():
    """Returns stats"""
    classes = {"amenities": "Amenity",
               "cities": "City",
               "places": "Place",
               "reviews": "Review",
               "states": "State",
               "users": "User"}
    for key, value in classes.items():
        classes[key] = storage.count(value)
    return jsonify(classes)

#!/usr/bin/python3
"""Script that starts a Flask web application"""

from api.v1.views import app_views
from flask import Flask, jsonify
from models import storage
from os import getenv


flk = Flask(__name__)
flk.register_blueprint(app_views)


@flk.teardown_appcontext
def close_storage():
    """Close storage"""
    storage.close()


@flk.errorhandler(404)
def page_not_found():
    """Page not found"""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    flk.run(host=getenv('HBNB_API_HOST'),
            port=getenv('HBNB_API_PORT'), threaded=True)

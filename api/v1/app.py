#!/usr/bin/python3
"""Script that starts a Flask web application"""

from api.v1.views import app_views
from flask import Flask, jsonify
from models import storage
from os import getenv


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_storage(exception):
    """Close storage"""
    storage.close()


@app.errorhandler(404)
def page_not_found(exception):
    """Page not found"""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = getenv("HBNB_API_HOST") if getenv("HBNB_API_HOST") else '0.0.0.0'
    port = getenv("HBNB_API_PORT") if getenv("HBNB_API_PORT") else 5000
    app.run(host=host, port=port, threaded=True)

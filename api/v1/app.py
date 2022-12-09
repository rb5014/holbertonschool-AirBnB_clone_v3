#!/usr/bin/python3
"""This module contains variables and methods used to connect to API
"""
from os import getenv
from flask import Flask, jsonify, Blueprint
from models import storage
from api.v1.views import app_views
from flask_cors import CORS


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True

@app.teardown_appcontext
def teardown(exception):
    """Remove the current SQLAlchemy session."""
    storage.close()


@app.errorhandler(404)
def not_found(err):
    """return an error for 404 not found"""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    app.run(host=getenv("HBNB_API_HOST", default="0.0.0.0"),
            port=getenv("HBNB_API_PORT", default=5000), threaded=True)

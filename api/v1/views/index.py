#!/usr/bin/python3
"""Index fiile of the api"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route("/status", methods=['GET'], strict_slashes=False)
def status():
    """get status"""
    return jsonify(status="OK")

#!/usr/bin/python3
"""Index fiile of the api"""
from api.v1.views import app_views
import json


@app_views.route("/status", strict_slashes=False)
def status():
    return json.dumps({"status": "OK"}, indent=4)

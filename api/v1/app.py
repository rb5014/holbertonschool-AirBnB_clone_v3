#!/usr/bin/python3
"""Api of the project airbnbclone
"""
from flask import Flask
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    """Remove the current SQLAlchemy session."""
    storage.close()


host = "0.0.0.0"
if getenv("HBNB_API_HOST"):
    host = getenv("HBNB_API_HOST")

port = 5000
if getenv("HBNB_API_PORT"):
    try:
        port = int(getenv("HBNB_API_HOST"))
    except Exception:
        pass

if __name__ == "__main__":
    app.run(host=host, port=port, threaded=True)

#!/usr/bin/python3
"""app.py to connect to API"""
from api.v1.views import app_views
from flask import Flask, make_response, jsonify
from models import storage
import os

app = Flask(__name__)

app.url_map.strict_slashes = False

# flask server environmental setup
host = os.getenv('HBNB_API_HOST', '0.0.0.0')
port = os.getenv('HBNB_API_PORT', 5000)

app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_appcontext(code):
    """teardown_appcontext"""
    storage.close()


@app.errorhandler(404)
def not_found(e):
    """404 error handler"""
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    """
    MAIN Flask App
    """
    app.run(host=host, port=port)

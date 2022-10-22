#!/usr/bin/python3
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models import *


@app_views.route('/status')
def status():
    return jsonify({"status": "OK"})

@app_views.route('/stats')
def stats():
    # classes = [Amenity, City, Place, Review, State, User]
    
    return jsonify({
        "amenities": storage.count(Amenity),
        "cities": storage.count(City),
        "places": storage.count(Place),
        "reviews": storage.count(Review),
        "states": storage.count(State),
        "users": storage.count(User)
    })

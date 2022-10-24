#!/usr/bin/python3
"""index.py routes to connect to API"""
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.city import City
from models.state import State


@app_views.route('states/<state_id>/cities/', methods=['GET'])
def get_state_cities(state_id):
    """get cities in a specified state"""
    state = storage.get(State, state_id)
    if state is None:
        return abort(404)
    cities = []
    """Retrieves City objects"""
    for city in storage.all(City).values():
        if city.state_id == state_id:
            cities.append(city.to_dict())
    return jsonify(cities)


@app_views.route('/cities/<city_id>', methods=['GET'])
def get_city(city_id):
    """Gets City object by id"""
    city = storage.get(City, city_id)
    if city is None:
        return abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    """Deletes City object by id"""
    city = storage.get(City, city_id)
    if city is None:
        return abort(404)
    city.delete()
    storage.save()
    return jsonify({})


@app_views.route('/states/<state_id>/cities', methods=['POST'])
def post_city(state_id):
    """Create City object"""
    state = storage.get(State, state_id)
    if state is None:
        return abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    elif 'name' not in request.get_json():
        return make_response(jsonify({'error': 'Missing name'}), 400)
    city = City(**request.get_json())
    city.state_id = state_id
    city.save()
    return make_response(jsonify(city.to_dict()), 201)


@app_views.route('cities/<city_id>', methods=['PUT'])
def put_city(city_id):
    """Updates City object"""
    city = storage.get(City, city_id)
    if city is None:
        return abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    elif 'name' not in request.get_json():
        return make_response(jsonify({'error': 'Missing name'}), 400)

    for key, value in request.get_json().items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(city, key, value)
    city.save()
    return make_response(jsonify(city.to_dict()), 200)

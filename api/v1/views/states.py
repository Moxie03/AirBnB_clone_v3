#!/usr/bin/python3
"""index.py routes to connect to API"""
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.state import State


@app_views.route('/states/', methods=['GET'])
def get_states():
    states = []
    """Retrieves all State objects"""
    for obj in storage.all(State).values():
        states.append(obj.to_dict())
    return jsonify(states)


@app_views.route('/states/<state_id>', methods=['GET'])
def get_state(state_id):
    """Gets State object by id"""
    state = storage.get(State, state_id)
    if state is None:
        return abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """Deletes State object by id"""
    state = storage.get(State, state_id)
    if state is None:
        return abort(404)
    state.delete()
    storage.save()
    return jsonify({})


@app_views.route('/states/', methods=['GET', 'POST'])
def post_state():
    """Create State object"""
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    elif 'name' not in request.get_json():
        return make_response(jsonify({'error': 'Missing name'}), 400)
    state = State(**request.get_json())
    state.save()
    return make_response(jsonify(state.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'])
def put_state(state_id):
    """Updates a State object"""
    state = storage.get(State, state_id)
    if state is None:
        return abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    elif 'name' not in request.get_json():
        return make_response(jsonify({'error': 'Missing name'}), 400)

    for key, value in request.get_json().items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(state, key, value)
    state.save()
    return make_response(jsonify(state.to_dict()), 200)

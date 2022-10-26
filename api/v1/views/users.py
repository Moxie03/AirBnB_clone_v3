#!/usr/bin/python3
"""usersw.py routes to connect to API"""
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route('/users/', methods=['GET'])
def get_users():
    """Retrieves all User objects"""
    users = []
    for obj in storage.all(User).values():
        users.append(obj.to_dict())
    return jsonify(users)


@app_views.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    """Gets User object by id"""
    user = storage.get(User, user_id)
    if user is None:
        return abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Deletes City object by id"""
    user = User.get(User, user_id)
    if user is None:
        return abort(404)
    user.delete()
    storage.save()
    return jsonify({})


@app_views.route('/users/', methods=['POST'])
def post_user():
    """Create User object"""
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    elif 'email' not in request.get_json():
        return make_response(jsonify({'error': 'Missing email'}), 400)
    elif 'password' not in request.get_json():
        return make_response(jsonify({'error': 'Missing password'}), 400)
    user = User(**request.get_json())
    user.save()
    return make_response(jsonify(user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'])
def put_user(user_id):
    """Updates User object"""
    user = storage.get(User, user_id)
    if user is None:
        return abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    elif 'email' not in request.get_json():
        return make_response(jsonify({'error': 'Missing email'}), 400)
    elif 'password' not in request.get_json():
        return make_response(jsonify({'error': 'Missing password'}), 400)

    for key, value in request.get_json().items():
        if key not in ["id", "email", "created_at", "updated_at"]:
            setattr(user, key, value)
    user.save()
    return make_response(jsonify(user.to_dict()), 200)

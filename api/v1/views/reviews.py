#!/usr/bin/python3
"""index.py routes to connect to API"""
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.place import Place
from models.review import Review


@app_views.route('/places/<place_id>/reviews/', methods=['GET'])
def get_place_reviews(place_id):
    """get reviews in a specified place"""
    place = storage.get(State, place_id)
    if place is None:
        return abort(404)
    reviews = []
    for review in storage.all(Review).values():
        if review.place_id == place_id:
            reviews.append(review.to_dict())
    return jsonify(reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'])
def get_review(review_id):
    """Gets Review object by id"""
    review = storage.get(Review, review_id)
    if review is None:
        return abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def delete_review(review_id):
    """Deletes Review object by id"""
    review = storage.get(Review, review_id)
    if review is None:
        return abort(404)
    review.delete()
    storage.save()
    return jsonify({})


@app_views.route('/places/<place_id>/reviews', methods=['POST'])
def post_review(place_id):
    """Create Review object"""
    place = storage.get(Place, place_id)
    if place is None:
        return abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    elif 'name' not in request.get_json():
        return make_response(jsonify({'error': 'Missing name'}), 400)
    review = Review(**request.get_json())
    review.place_id = place_id
    review.save()
    return make_response(jsonify(review.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'])
def put_review(review_id):
    """Updates Review object"""
    review = storage.get(Review, review_id)
    if review is None:
        return abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    elif 'name' not in request.get_json():
        return make_response(jsonify({'error': 'Missing name'}), 400)

    for key, value in request.get_json().items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(review, key, value)
    review.save()
    return make_response(jsonify(review.to_dict()), 200)

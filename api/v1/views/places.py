#!/usr/bin/python3
"""index.py routes to connect to API"""
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.city import City
from models.place import Place
from models.state import State


@app_views.route('/cities/<city_id>/places/', methods=['GET'])
def get_city_places(city_id):
    """Retrieves all Place objects"""
    city = storage.get(City, city_id)
    if city is None:
        return abort(404)
    places = []
    for place in storage.all(Place).values():
        if place.city_id == city_id:
            places.append(place.to_dict())
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'])
def get_place(place_id):
    """Gets Place object by id"""
    place = storage.get(Place, place_id)
    if place is None:
        return abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_places(place_id):
    """Deletes Place object by id"""
    place = storage.get(Place, place_id)
    if place is None:
        return abort(404)
    place.delete()
    storage.save()
    return jsonify({})


@app_views.route('/cities/<city_id>/places/', methods=['POST'])
def post_place(city_id):
    """Create Place object"""
    city = storage.get(City, city_id)
    if city is None:
        return abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'user_id' not in request.get_json():
        return make_response(jsonify({'error': 'Missing user_id'}), 400)
    user = storage.get(User, request.get_json()['user_id'])
    if user is None:
        abort(404)
    if 'name' not in request.get_json():
        return make_response(jsonify({'error': 'Missing name'}), 400)
    place = Place(**request.get_json())
    place.city_id = city_id
    storage.save()
    return make_response(jsonify(place.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'])
def put_place(place_id):
    """Updates Place object"""
    place = storage.get(Place, place_id)
    if place is None:
        return abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for key, value in request.get_json().items():
        if key not in ["id", "created_at", "updated_at", "user_id", "city_id"]:
            setattr(place, key, value)
    storage.save()
    return make_response(jsonify(place.to_dict()), 200)


@app_views.route('/places_search', methods=['POST'])
def post_places_search():
    """searches for a place"""
    if request.get_json() is None:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    params = request.get_json()
    states = params.get('states', [])
    cities = params.get('cities', [])
    amenities = params.get('amenities', [])
    amenity_objects = []
    for amenity_id in amenities:
        amenity = storage.get(Amenity, amenity_id)
        if amenity:
            amenity_objects.append(amenity)
    if states == cities == []:
        places = storage.all('Place').values()
    else:
        places = []
        print(len(states))
        for state_id in states:
            print(f'ss: {state_id}')
            state = storage.get(State, state_id)
            state_cities = state.cities
            for city in state_cities:
                if city.id not in cities:
                    cities.append(city.id)
        for city_id in cities:
            city = storage.get(City, city_id)
            for place in city.places:
                places.append(place)
    confirmed_places = []
    for place in places:
        place_amenities = place.amenities
        confirmed_places.append(place.to_dict())
        for amenity in amenity_objects:
            if amenity not in place_amenities:
                confirmed_places.pop()
                break
    return jsonify(confirmed_places)

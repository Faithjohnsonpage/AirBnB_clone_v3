#!/usr/bin/python3
"""Flask module to handle place amenities."""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.base_model import BaseModel
from models.place import Place
from models.user import User
from models.amenity import Amenity


@app_views.route('/places/<string:place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def place_amenities(place_id):
    """Get amenities associated with a place.

    Args:
        place_id (str): The ID of the place to retrieve amenities for.

    Returns:
        JSON: A JSON response containing a list of amenities associated
        with the place.
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    place_amenities = [amenity.to_dict() for amenity in place.amenities]
    return jsonify(place_amenities)


@app_views.route('/places/<string:place_id>/amenities/<string:amenity_id>',
                 methods=['POST', 'DELETE'], strict_slashes=False)
def place_amenity_link_unlink(place_id, amenity_id):
    """Link or unlink an amenity to/from a place.

    Args:
        place_id (str): The ID of the place to link/unlink the amenity to/from
        amenity_id (str): The ID of the amenity to link/unlink.

    Returns:
        JSON: A JSON response indicating the success of the operation.
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    if request.method == 'DELETE':
        if amenity not in place.amenities:
            abort(404)
        place.amenities.remove(amenity)
        storage.save()
        return jsonify({}), 200

    elif request.method == 'POST':
        if amenity in place.amenities:
            return jsonify(amenity.to_dict()), 200
        place.amenities.append(amenity)
        storage.save()
        return jsonify(amenity.to_dict()), 201

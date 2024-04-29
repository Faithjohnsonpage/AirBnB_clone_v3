#!/usr/bin/python3
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


stats = {
  "amenities": 0,
  "cities": 0,
  "places": 0,
  "reviews": 0,
  "states": 0,
  "users": 0
}

# Mapping stats keys to corresponding classes
class_mapping = {
    "amenities": Amenity,
    "cities": City,
    "places": Place,
    "reviews": Review,
    "states": State,
    "users": User
}


@app_views.route('/status', methods=["GET"])
def view_status():
    """Returns a JSON response with status OK."""
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=["GET"])
def get_stats():
    """ Endpoint for getting counts of all object types """
    for key, value in stats.items():
        # Use the class_mapping dict to get the class corresponding to the key
        obj_class = class_mapping[key]
        each_count = storage.count(obj_class)
        stats[key] = each_count
    return jsonify(stats)

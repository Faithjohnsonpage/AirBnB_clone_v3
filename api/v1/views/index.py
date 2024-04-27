#!/usr/bin/python3
from api.v1.views import app_views
from flask import jsonify


view = {
    "status": "OK"
}

@app_views.route('/status', methods=["GET"])
def view_status():
    """Returns a JSON response with status OK."""
    return jsonify(view)

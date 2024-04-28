#!/usr/bin/python3
"""
Main module of the AirBnB Clone RESTful API
"""
from flask import Flask, make_response, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv


app = Flask(__name__)

# Ensure JSON responses are always pretty-printed
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

# Register blueprint
app.register_blueprint(app_views)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({"error": "Not found"}), 404)

@app.teardown_appcontext
def close_storage(self):
    """
    Method to close the storage engine
    """
    storage.close()


if __name__ == "__main__":
    # Get API host and port from environment variables
    host = getenv('HBNB_API_HOST', default='0.0.0.0')
    port = getenv('HBNB_API_PORT', default=5000)

    # Run the Flask app
    app.run(host=host, port=int(port), threaded=True)

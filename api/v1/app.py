#!/usr/bin/python3
"""
Main module of the AirBnB Clone RESTful API
"""
from flask import Flask
from models import storage
from api.v1.views import app_views
from os import getenv


app = Flask(__name__)

# Register blueprint
app.register_blueprint(app_views)


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

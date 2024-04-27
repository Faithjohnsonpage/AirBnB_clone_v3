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
    api_host = getenv("HBNB_API_HOST")
    api_port = getenv("HBNB_API_PORT")

    # Run the Flask app
    app.run(host=api_host if api_host else '0.0.0.0',
            port=int(api_port) if api_port else 5000, threaded=True)


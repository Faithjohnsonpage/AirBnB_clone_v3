#!/usr/bin/python3
from flask import Blueprint

# Create a Blueprint object for v1 views
app_views = Blueprint('views', __name__, url_prefix='/api/v1')

# Import views from index module
from api.v1.views.index import *

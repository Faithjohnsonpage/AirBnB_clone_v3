#!/usr/bin/python3
from flask import Blueprint

# Create a Blueprint object for v1 views
app_views = Blueprint('views', __name__, url_prefix='/api/v1')

from api.v1.views.index import *
from api.v1.views.state import *
from api.v1.views.city import *

#!/usr/bin/python3
"""Initialize app_views Blueprint views"""
from flask import Blueprint

app_views = Blueprint("app_views", __name__)

from api.v1.views.index import *

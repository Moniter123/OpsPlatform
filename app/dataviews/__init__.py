from flask import Blueprint

dataviews = Blueprint('dataviews', __name__)

from . import forms, views

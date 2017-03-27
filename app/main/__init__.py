# app/main/__init__.py

from flask import Blueprint

main = Blueprint('main', __name__)

from . import views, errors

from flask import Blueprint
from flask_restful import Api


store = Blueprint('store', __name__)
store_api = Api(store)

from . import resource

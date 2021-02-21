from flask import Blueprint
from flask_restplus import Api


item = Blueprint('item', __name__)
item_api = Api(item)

from . import resource

import os
from app import create_app, db
from flask_migrate import Migrate
from flask_restplus import Api
from flask_jwt_extended import JWTManager
from app.item import item_api as ns1

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)
api = Api(app, doc='/doc')

ns = api.namespace('FlaskStore', 
                   description='Flask Store Swagger')

api.add_namespace(ns1)

jwt = JWTManager(app)

@app.before_first_request
def create_tables():
    db.create_all()

import os
from app import create_app, db
from flask_migrate import Migrate
from flask_restful import Api
from flask_jwt_extended import JWTManager
from app.resources import Item, ItemList, Store, StoreList

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)
api = Api(app)

jwt = JWTManager(app)

@app.before_first_request
def create_tables():
    db.create_all()

api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')

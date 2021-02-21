from . import item_api
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from .model import Item as ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field cannot be None!"
    )
    parser.add_argument('store_id',
        type=int,
        required=True,
        help="Every item needs a store_id."
    )
    
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return {'item': item.json()}, 200
        return {'message': 'Item not found'}, 404
    
    @jwt_required()
    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists.".format(name)}, 400

        data = Item.parser.parse_args()
        item = ItemModel(name, **data)
        
        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred inserting the item."}, 500
        return item.json(), 201
    
    @jwt_required()
    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {'message': 'Item deleted.'}
        return {'message': 'Item not found.'}, 404
    
    @jwt_required()
    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        if item:
            item.price = data['price']
        else:
            item = ItemModel(name, **data)
        item.save_to_db()
        return item.json()


class ItemList(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}


item_api.add_resource(Item, '/item/<string:name>')
item_api.add_resource(ItemList, '/items')

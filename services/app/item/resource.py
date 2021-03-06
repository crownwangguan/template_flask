from flask_restplus import Resource, Namespace, fields
from flask_jwt_extended import jwt_required
from .model import Item as ItemModel
from .schema import ItemSchema
from marshmallow import ValidationError
from flask_restful import request

api = Namespace('items', path='/', description='Operations related to items')


item = api.model('Item', {
    'name': fields.String(description='Item name', required=True),
    'price': fields.Float(description='Item price', required=True),
    'store_id': fields.Integer(description='Store ID', required=True),
})

item_schema = ItemSchema()
item_list_schema = ItemSchema(many=True)

@api.doc(params={'name': 'Item name'})
class Item(Resource):

    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item_schema.dump(item), 200
        return {'message': 'Item not found'}, 404

    @jwt_required()
    @api.expect(item)
    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists.".format(name)}, 400

        item_json = request.get_json()
        item_json["name"] = name

        try:
            item = item_schema.load(item_json)
        except ValidationError as err:
            return err.messages, 400

        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred while inserting the item."}, 500

        return item_schema.dump(item), 201

    @jwt_required()
    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {'message': 'Item deleted.'}
        return {'message': 'Item not found.'}, 404

    @jwt_required()
    @api.expect(item)
    def put(self, name):
        item_json = request.get_json()
        item = ItemModel.find_by_name(name)

        if item:
            item.price = item_json["price"]
        else:
            item_json["name"] = name

            try:
                item = item_schema.load(item_json)
            except ValidationError as err:
                return err.messages, 400

        item.save_to_db()

        return item_schema.dump(item), 200


class ItemList(Resource):
    @classmethod
    def get(cls):
        return {"items": item_list_schema.dump(ItemModel.find_all())}, 200


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')

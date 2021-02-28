from flask_restplus import Resource, Namespace, fields
from flask_jwt_extended import jwt_required
from .model import Item as ItemModel

api = Namespace('items', path='/', description='Operations related to items')


item = api.model('Item', {
    'name': fields.String(description='Item name', required=True),
    'price': fields.Float(description='Item price', required=True),
    'store_id': fields.Integer(description='Store ID', required=True),
})


@api.doc(params={'name': 'Item name'})
class Item(Resource):
    parser = api.parser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot be None!")
    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help="Every item needs a store_id.")

    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return {'item': item.json()}, 200
        return {'message': 'Item not found'}, 404

    @jwt_required()
    @api.expect(item)
    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists.".format(name)}, 400

        data = Item.parser.parse_args()
        item = ItemModel(name, **data)

        try:
            item.save_to_db()
        except Exception:
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
    @api.expect(item)
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


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')

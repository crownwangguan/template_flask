from flask_restplus import Resource, Namespace, fields
from flask_jwt_extended import jwt_required
from .model import OrderModel, ItemsInOrder
from ..item.model import Item as ItemModel
from flask import request
from .schema import ItemsInOrderSchema, OrderSchema


api = Namespace('orders', path='/', description='Operations related to orders')
orderSchema = OrderSchema()


itemsInOrder = api.model('ItemsInOrder', {
    "name": fields.String(description='Item name', required=True),
    "qty": fields.Integer(description='Item quantity', required=True),
})

order = api.model('Order', {
    "items": fields.List(fields.Nested(itemsInOrder)),
})

class Order(Resource):
    @classmethod
    @jwt_required()
    @api.expect(order)
    def post(cls):
        data = request.get_json()
        items = []
        ordered_list = data['items'] # list of dictionaries

        for ordered_item in ordered_list:
            name = ordered_item['name']
            count = ordered_item['qty']
            res = ItemModel.find_by_name(name)
            if not res:
                return {"msg": "Item not present {}".format(name)},404
            items.append(ItemsInOrder(item_id=ItemModel.find_id(name), quantity=count))
        print(items)

        order = OrderModel(items=items)
        order.save_to_db()  #save orders to database

        return orderSchema.dump(order), 201

api.add_resource(Order, "/order")

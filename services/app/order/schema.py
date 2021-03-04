from .. import ma
from marshmallow import fields
from .model import ItemsInOrder, OrderModel


class ItemsInOrderSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ItemsInOrder
        load_instance = True
        load_only = ("order",)
        include_fk= True
        

class OrderSchema(ma.SQLAlchemyAutoSchema):
    items = ma.Nested(ItemsInOrderSchema, many=True)

    class Meta:
        model = OrderModel
        load_instance = True
        include_fk = True
    
    total_price = fields.Method("get_balance", deserialize="load_balance")

    def get_balance(self, obj):
        return obj.amount

    def load_balance(self, value):
        return float(value)

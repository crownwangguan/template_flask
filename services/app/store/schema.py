from .. import ma
from .model import Store
from ..item.model import Item
from ..item.schema import ItemSchema


class StoreSchema(ma.SQLAlchemyAutoSchema):
    items = ma.Nested(ItemSchema, many=True)

    class Meta:
        model = Store
        dump_only = ("id",)
        include_fk = True
        load_instance = True

from .. import ma
from .model import Item
from ..store.model import Store


class ItemSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Item
        load_only = ("store",)
        dump_only = ("id",)
        include_fk = True
        load_instance = True

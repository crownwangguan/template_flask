from .. import ma
from ..models import User


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        fields = ("email", "username", "password")
        model = User
        load_only = ("password",)
        dump_only = ("id",)
        load_instance = True

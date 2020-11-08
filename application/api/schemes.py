import json

from application import ma
from application.api.models import User


class ResponseBasicSchema(ma.Schema):
    status = ma.Str()
    msg = ma.Str()

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        fields = ['username', 'email', 'active']


class UserWithPasswordSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'active']


class FullUserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'active', 'created']


class ResponseUserSchema(ma.Schema):
    status = ma.Str()
    msg = ma.Str()
    data = ma.Nested(FullUserSchema)


class ResponseUserWithTokenSchema(ResponseUserSchema):
    token = ma.Str()


class ResponseListUsersSchema(ma.Schema):
    status = ma.Str()
    msg = ma.Str()
    data = ma.List(ma.Nested(FullUserSchema))


class LoginSchema(ma.Schema):
    email = ma.Str()
    password = ma.Str()


class ResponseLoginSchema(ma.Schema):
    status = ma.Str()
    msg = ma.Str()
    token = ma.Str()
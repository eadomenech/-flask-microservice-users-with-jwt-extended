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


class ResponseUserSchema(ma.Schema):
    status = ma.Str()
    msg = ma.Str()
    data = ma.Nested(UserSchema)


class ResponseUserWithTokenSchema(ResponseUserSchema):
    token = ma.Str()


class ResponseListUsersSchema(ma.Schema):
    status = ma.Str()
    msg = ma.Str()
    data = ma.List(ma.Nested(UserSchema))


class LoginSchema(ma.Schema):
    email = ma.Str()
    password = ma.Str()


class ResponseLoginSchema(ma.Schema):
    status = ma.Str()
    msg = ma.Str()
    token = ma.Str()
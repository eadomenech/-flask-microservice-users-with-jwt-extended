from flask import Blueprint, request
from apifairy import response, body, other_responses
from sqlalchemy import exc, or_
from flask_jwt_extended import (
    create_access_token, jwt_required, get_jwt_identity)

from application import db, bcrypt
from application.api.schemes import (
    ResponseBasicSchema, ResponseUserSchema, LoginSchema, ResponseLoginSchema,
    ResponseUserWithTokenSchema, UserWithPasswordSchema)
from application.api.models import User


api = Blueprint('auth', __name__)


@api.route('/login', methods=['POST'])
@body(LoginSchema)
@response(ResponseLoginSchema, description='Successfully logged in.')
@other_responses({400: 'Invalid request.', 404: 'User not fount'})
def login(credentials):
    """
    Login

    Login endpoint.
    """
    post_data = request.get_json()
    response_object = {
        'status': 'fail',
        'msg': 'Invalid request.',
        'token': '',
    }
    email = post_data.get('email')
    password = post_data.get('password')
    try:
        # fetch the user data
        user = User.query.filter_by(email=email).first()
        if user:
            if bcrypt.check_password_hash(
                    user.password, password.encode('utf-8')):
                auth_token = create_access_token(identity=email)
                if auth_token:
                    response_object['status'] = 'success'
                    response_object['msg'] = 'Successfully logged in.'
                    response_object['token'] = auth_token
                    return response_object, 200
            else:
                response_object['msg'] = 'Incorrect password.'
        else:
            response_object['msg'] = 'User does not exist.'
        return response_object, 404
    except Exception as e:
        response_object['msg'] = 'Try again.'
        return response_object, 500


@api.route('/logout', methods=['GET'])
@response(ResponseBasicSchema, description='Successfully logged out.')
@other_responses({401: 'Unauthorized.', 403: 'Forbidden.'})
@jwt_required
def logout():
    """
    Logout

    Logout endpoint.
    """
    response_object = {
        'status': 'fail',
        'msg': 'Provide a valid auth token.'
    }
    current_user = get_jwt_identity()
    if current_user:
        response_object['status'] = 'success'
        response_object['msg'] = 'Successfully logged out.'
        return response_object, 200
    return response_object, 401


@api.route('/register', methods=['POST'])
@body(UserWithPasswordSchema)
@response(
    ResponseUserWithTokenSchema, status_code=201,
    description='Successfully registered.')
@other_responses({400: 'Invalid request.'})
def register(user):
    """
    Register a user

    This endpoint register a user.
    """
    post_data = request.get_json()
    response_object = {
        'status': 'fail',
        'msg': 'Invalid payload.',
        'data': {}
    }
    username = post_data.get('username')
    email = post_data.get('email')
    password = post_data.get('password')
    try:
        user = User.query.filter(
            or_(User.username == username, User.email == email)).first()
        if not user:
            new_user = User(
                username=username, email=email, password=password)
            db.session.add(new_user)
            db.session.commit()
            response_object['status'] = 'success'
            response_object['msg'] = 'Successfully registered.'
            return response_object, 201
        else:
            message = 'Sorry. That user already exists.'
            response_object['msg'] = message
            return response_object, 400
    except exc.IntegrityError:
        db.session.rollback()
        return response_object, 400


@api.route('/status', methods=['GET'])
@response(ResponseUserSchema, description='Success.')
@other_responses({401: 'Unauthorized.'})
@jwt_required
def status():
    """
    User status

    User status endpoint.
    """
    response_object = {
        'status': 'fail',
        'msg': 'Provide a valid auth token.'
    }
    current_user = get_jwt_identity()
    user = User.query.filter_by(email=current_user).first()
    response_object['status'] = 'success'
    response_object['msg'] = 'Success.'
    response_object['data'] = user.to_json()
    return response_object, 200
from flask_restplus import Resource, Namespace, fields
from flask import request
from .schema import UserSchema
from ..models import User
import datetime
from marshmallow import ValidationError
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity
)


api = Namespace('auth', path='/api', description='Operations related to login')


user = api.model('User', {
    'email': fields.String(description='User email', required=True),
    'password': fields.Float(description='User password', required=True)
})

user_schema = UserSchema()

class UserRegister(Resource):
    @api.expect(user)
    @classmethod
    def post(cls):
        try:
            user = user_schema.load(request.get_json())
        except ValidationError as err:
            return err.messages, 400
        
        user_exists = User.query.filter_by(
                email=user.email
            ).first()
        if user_exists:
            return {
                "message": "A user with that username already exists."
                }, 400
        user.save_to_db()
        return {"message": "User created successfully."}, 201

class UserLogin(Resource):
    @api.expect(user)
    def post(self):
        try:
            user_json = request.get_json()
            user_data = user_schema.load(user_json)
        except ValidationError as err:
            print(err)
            return err.messages, 400
        try:
            # fetch the user data
            user = User.query.filter_by(
                email=user_data.email
            ).first()

            if user and user.verify_password(user_json["password"]):
                access_token = create_access_token(identity=user.id, fresh=True)
                refresh_token = create_refresh_token(user.id)
                
                return {
                    "access_token": access_token,
                    "refresh_token": refresh_token
                }, 200
            else:
                responseObject = {
                    'status': 'fail',
                    'message': 'User does not exist.'
                }
                return responseObject, 404
        except Exception as e:
            print(e)
            responseObject = {
                'status': 'fail',
                'message': 'Try again'
            }
            return responseObject, 500


class TokenRefresh(Resource):
    @classmethod
    @jwt_required(refresh=True)
    def post(cls):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, 
                                        fresh=True)
        return {"access_token": new_token}, 200

api.add_resource(UserLogin, '/login')
api.add_resource(UserRegister, '/register')
api.add_resource(TokenRefresh, '/refresh')

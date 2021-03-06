from flask_restplus import Resource, Namespace, fields
from flask import request
from .schema import UserSchema
from ..models import User
from marshmallow import ValidationError


api = Namespace('auth', path='/api', description='Operations related to login')


user = api.model('User', {
    'email': fields.String(description='User email', required=True),
    'password': fields.Float(description='User password', required=True)
})

user_schema = UserSchema()

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
                auth_token = user.encode_auth_token(user.id)
                if auth_token:
                    responseObject = {
                        'status': 'success',
                        'message': 'Successfully logged in.',
                        'auth_token': auth_token
                    }
                    return responseObject, 200
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

api.add_resource(UserLogin, '/login')

from flask_restplus import Resource, Namespace, fields
from flask import make_response, jsonify
from ..models import User


api = Namespace('auth', path='/api', description='Operations related to login')


user = api.model('User', {
    'email': fields.String(description='User email', required=True),
    'password': fields.Float(description='User password', required=True)
})

class UserLogin(Resource):
    parser = api.parser()
    parser.add_argument('email',
                        type=str,
                        required=True,
                        help="This field cannot be None!")
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="User password is needed!")

    @api.expect(user)
    def post(self):
        # get the post data
        post_data = UserLogin.parser.parse_args()
        try:
            # fetch the user data
            user = User.query.filter_by(
                email=post_data.get('email')
            ).first()
            if user and user.verify_password(post_data.get('password')):
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

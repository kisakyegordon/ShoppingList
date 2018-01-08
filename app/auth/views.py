from . import auth_blueprint
from flask_bcrypt import Bcrypt
from flask.views import MethodView
from flask import Blueprint, make_response, request, jsonify
from app.models import User
from flask import json, abort, request, jsonify
from werkzeug.exceptions import HTTPException, NotFound, BadRequest



class RegistrationView(MethodView):
    '''
    Registration View Class
    '''

    def post(self):
        ''' POST method for Registration '''
        if not request.data:
            return make_response(jsonify({"message":"Enter your user login details"})), 400

        user = User.query.filter_by(email=request.data['email']).first()

        if not user:
            if '@' not in request.data['email']:
                return make_response(jsonify({"message":"Enter a valid email address"})), 400
            else:
                try:
                    post_data = request.data
                    email = post_data['email']
                    password = post_data['password']
                    country_town = post_data['country_town']

                    user = User(email=email, password=password, country_town=country_town)
                    user.save()

                    response = {
                        'message': 'You registered successfully.'
                        }

                    return make_response(jsonify(response)), 201
                except Exception as e:

                    response = {
                        "message": str(e) + "Missing"
                    }
                    return make_response(jsonify(response)), 400
        else:
            response = {
                'message': 'User Already Exists. Please Login.'
            }
            return make_response(jsonify(response)), 409


class LoginView(MethodView):
    '''
    Login view class
    '''

    def post(self):
        ''' POST method for Login ''' 
        try:
            user = User.query.filter_by(email=request.data['email']).first()

            if user and user.password_is_valid(request.data['password']):
                access_token = user.generate_token(user.id)
                if access_token:

                    user.token = access_token.decode()
                    user.save()

                    response = {
                        'Hello': 'Welcome',
                        'message': 'Successfully LoggedIn',
                        'access_token': access_token.decode()
                    }
                    return make_response(jsonify(response)), 200
            else:
                response = {
                    'message': 'Invalid email or password'
                }
                return make_response(jsonify(response)), 400
        except Exception as e:
            response = {
                'message': json.loads(str(e))
            }
            return make_response(jsonify(response)), 500

class LogoutView(MethodView):
    '''
    Logout view class
    '''

    def post(self):
        ''' POST method for Logout '''

        auth_header = request.headers.get("Authorization")
        access_token = auth_header.split(" ")[1]

        if access_token:
            user_id = User.decode_token(access_token)
            if isinstance(user_id, int):
                user_id = User.decode_token(access_token)
                user = User.query.filter_by(id=user_id).first()

                if user:
                    user.token = ''
                    user.save()

                response = {
                    'message': 'Logged Out Successfully'
                }

                return make_response(jsonify(response)), 200


class ResetView(MethodView):
    '''
    ResetView view class
    '''

    def post(self):
        ''' POST method for ResetView '''

        email = request.data['email']
        country_town = request.data['country_town']

        user = User.query.filter_by(email=email).filter_by(country_town=country_town).first()

        if not user:
            return make_response(jsonify({'message':'No User Found'})), 404

        user.password = Bcrypt().generate_password_hash(request.data['password']).decode()   
        user.save()
        response = {'message': 'Password Succesfully Changed'}
        return make_response(jsonify(response)), 200



registration_view = RegistrationView.as_view('registration_view')
login_view = LoginView.as_view('login_view')
logout_view = LogoutView.as_view('logout_view')
reset_view = ResetView.as_view('reset_view')

auth_blueprint.add_url_rule(
    '/api/v2/auth/register',
    view_func=registration_view,
    methods=['POST'])

auth_blueprint.add_url_rule(
    '/api/v2/auth/login',
    view_func=login_view,
    methods=['POST']
)

auth_blueprint.add_url_rule(
    '/api/v2/auth/logout',
    view_func=logout_view,
    methods=['POST']
)

auth_blueprint.add_url_rule(
    '/api/v2/auth/reset-password',
    view_func=reset_view,
    methods=['POST']
)

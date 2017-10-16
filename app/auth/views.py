from . import auth_blueprint
from flask_bcrypt import Bcrypt
from flask.views import MethodView
from flask import Blueprint, make_response, request, jsonify
from app.models import User
from flask import json, abort, request, jsonify


class RegistrationView(MethodView):

    def post(self):

        user = User.query.filter_by(email=request.data['email']).first()

        if not user:
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
                    'message': str(e)
                }
                return make_response(jsonify(response)), 401
        else:
            response = {
                'message': 'User Already Exists. Please Login.'
            }
            return make_response(jsonify(response)), 202


class LoginView(MethodView):

    def post(self):
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
                return make_response(jsonify(response)), 401
        except Exception as e:
            return abort(500, {'message': e})
            # response = {
            #     'message': json.loads(str(e))
            # }
            # return make_response(jsonify(response)), 500

class LogoutView(MethodView):
    
    def post(self):
        
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
    
    def post(self):
        data = request.get_json()
        # email = data['email']
        # user = User.query.filter_by(email=email).first()
        country_town = data['country_town']
        user = User.query.filter_by(country_town=country_town).first()
        if not user:
            return make_response(jsonify({'No User Found'})), 404
        user.password = Bcrypt().generate_password_hash(data['password']).decode()
        
        user.save()
        response = {'message': 'Password Succesfully Changed'}
        return make_response(jsonify(response)), 201



registration_view = RegistrationView.as_view('registration_view')
login_view = LoginView.as_view('login_view')
logout_view = LogoutView.as_view('logout_view')
reset_view = ResetView.as_view('reset_view')

auth_blueprint.add_url_rule(
    '/auth/register',
    view_func=registration_view,
    methods=['POST'])

auth_blueprint.add_url_rule(
    '/auth/login',
    view_func=login_view,
    methods=['POST']
)

auth_blueprint.add_url_rule(
    '/auth/logout',
    view_func=logout_view,
    methods=['POST']
)

auth_blueprint.add_url_rule(
    '/auth/reset-password',
    view_func=reset_view,
    methods=['POST']
)


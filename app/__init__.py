
# import json
from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from flask import request, jsonify, abort, make_response

from instance.config import app_config
# from flask_bcrypt import Bcrypt

db = SQLAlchemy()

def create_app(config_name):
    from app.models import ShoppingList, User
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config['config_name'])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    @app.route('/shoppinglists/', methods=['POST', 'GET'])
    @app.route('/shoppinglists/page=1', methods=['GET'])
    def shoppinglists():

        auth_header = request.headers.get("Authorization")
        access_token = auth_header.split(" ")[1]

        if access_token:
            user_id = User.decode_token(access_token)
            if not isinstance(user_id, str):

                if request.method == "POST":
                    name = str(request.data.get('name', ''))

                    if name:
                        shoppinglist = ShoppingList(name=name)
                        shoppinglist.save()
                        response = jsonify({
                            'id': shoppinglist.id,
                            'name': shoppinglist.name,
                            'owner': user_id
                        })
                        return make_response(response), 201

                elif request.method == "GET":

                    page = int(request.args['page'])
                    limit = int(request.args['limit'])

                    shoppinglist_get = ShoppingList.query.filter_by().paginate(page, limit, False).items
                    results = []

                    for shoppinglist in shoppinglist_get:
                        list_data = {}
                        list_data['id'] = shoppinglist.id
                        list_data['name'] = shoppinglist.name
                        list_data['owner'] = user_id
                        results.append(list_data)

                    url = '/shoppinglists/'
                    if page <= 1:
                        prev_url = ''
                    else:
                        page_value = page - 1
                        prev_url = url + '?limit={}&page={}'.format(limit, page_value)

                    next_url = url + '?limit={}&page={}'.format(limit, page + 1)

                    urls = {
                        'prev_url': prev_url,
                        'next_url': next_url
                    }


                    return make_response(jsonify(urls, results)), 200
            else:
                message = user_id
                response = {
                    'message': message
                }
                return make_response(jsonify(response)), 401

    @app.route('/shoppinglists/<int:id>', methods=['GET', 'DELETE', 'PUT'])
    def shopping_modifications(id, **kwargs):

        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[1]

        if access_token:
            user_id = User.decode_token(access_token)
            if not isinstance(user_id, str):
                shoppinglist = ShoppingList.query.filter_by(id=id).first()
                if not shoppinglist:
                    abort(404)

                if request.method == 'DELETE':
                    shoppinglist.delete()
                    return {"message" : "List {} Has Been Deleted".format(shoppinglist.name)}, 200

                elif request.method == 'PUT':
                    name = str(request.data.get('name', ''))
                    shoppinglist.name = name
                    shoppinglist.save()

                    response = jsonify({
                        'id': shoppinglist.id,
                        'name': shoppinglist.name
                    })
                    return make_response(response), 200
                else:
                    response = jsonify({
                        'id' : shoppinglist.id,
                        'name' : shoppinglist.name
                    })
                    return make_response(response), 200
            else:
                message = user_id
                response = {
                    'message': message
                }
                return make_response(jsonify(response)), 401

    from .auth import auth_blueprint
    app.register_blueprint(auth_blueprint)

    return app

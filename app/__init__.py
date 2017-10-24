import json
from functools import wraps
from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from flask import request, jsonify, abort, make_response, render_template
from instance.config import app_config
from flask_bcrypt import Bcrypt


db = SQLAlchemy()

def create_app(config_name):
    from app.models import ShoppingList, User, ListItem
    app = FlaskAPI(__name__, instance_relative_config=True)
    bcrypt = Bcrypt(app)


    app.config.from_object(app_config['development'])
    # app.config.from_object(app_config['production'])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    def login_essential(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            auth_header = request.headers.get("Authorization")

            if auth_header is not None and len(auth_header.split(" ")) == 2:
                access_token = auth_header.split(" ")[1]
                user_id = User.decode_token(access_token)
                if isinstance(user_id, int):

                    token_verify = User.query.filter_by(id=user_id).filter_by(token=access_token).first()
                    if token_verify:
                        return f(user_id)
                    else:
                        response = {'message': 'Token is unusable - login again'}
                        return make_response(jsonify(response)), 401
                else:
                    response = {'message': 'Token is Invalid'}
                    return make_response(jsonify(response)), 401

            else:
                response = {'message': 'No Token Provided'}
                return make_response(jsonify(response)), 401             

        return wrapper

    @app.route('/')
    def show_documentation():
        
        return render_template('index.html'), 200

    @app.route('/shoppinglists/', methods=['POST', 'GET'])
    @login_essential
    def shoppinglists(user_id):
        if request.method == "POST":
            name = str(request.data.get('name', ''))

            if name:
                shoppinglist = ShoppingList(name=name, owner=user_id)
                shoppinglist.save()
                response = jsonify({
                    'id': shoppinglist.id,
                    'name': shoppinglist.name,
                    'owner': user_id
                })
                return make_response(response), 201
            else:
                return make_response(jsonify({"message": "Please Enter Some Valid Content"})), 400

        elif request.method == "GET":

            if request.args.get("limit", "") and request.args.get("page", ""):
                page = int(request.args['page'])
                limit = int(request.args['limit'])

                shoppinglist_get = ShoppingList.query.filter_by(owner=user_id).paginate(page, limit, False).items
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


                return make_response(jsonify("Total = {} Lists".format(len(results)), urls, results)), 200

            else:
                shoppinglist_get = ShoppingList.query.filter_by(owner=user_id).all()
                results2 = []

                for shoppinglist in shoppinglist_get:
                    list_data = {}
                    list_data['id'] = shoppinglist.id
                    list_data['name'] = shoppinglist.name
                    list_data['owner'] = user_id
                    results2.append(list_data)

                return make_response(jsonify("Total = {} Lists".format(len(results2)), results2)), 200
                
    @app.route('/shoppinglists/search/', methods=['GET'])
    @login_essential
    def search(user_id):
        if request.args.get("q"):
        
            search_word = request.args.get("q", "")

            q = ShoppingList.query.filter(ShoppingList.name.ilike("%"+ search_word +"%")).filter_by(owner=user_id).all()

            results1 = []

            for shoppinglist in q:
                list_data = {}
                list_data['id'] = shoppinglist.id
                list_data['name'] = shoppinglist.name
                results1.append(list_data)

            return make_response(jsonify("Total = {} Search Results".format(len(results1)), results1)), 200
        else:
            return make_response(jsonify({'message':'Pass proper search parameters'}))
                        
        

    @app.route('/shoppinglists/<int:id>', methods=['GET', 'DELETE', 'PUT'])
    def shopping_modifications(id, **kwargs):
        
        auth_header = request.headers.get("Authorization")
            
        if auth_header is not None and len(auth_header.split(" ")) == 2:
            access_token = auth_header.split(" ")[1]
            user_id = User.decode_token(access_token)
            if isinstance(user_id, int):
        
                token_verify = User.query.filter_by(id=user_id).filter_by(token=access_token).first()
                if token_verify:
                    shoppinglist = ShoppingList.query.filter_by(id=id, owner=user_id).first()
                    if not shoppinglist:
                        response = {'message': 'List Does Not Exist'}
                        return make_response(jsonify(response)), 404 
                        # abort(404)

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
                    response = {'message': 'Token is unusable - login again'}
                    return make_response(jsonify(response)), 401
            else:
                response = {'message': 'Token is Invalid'}
                return make_response(jsonify(response)), 401

        else:
            response = {'message': 'No Token Provided'}
            return make_response(jsonify(response)), 401      

    @app.route('/shoppinglists/<int:list_id>/items/', methods=['POST', 'GET'])
    def listitems(list_id):
        
        auth_header = request.headers.get("Authorization")
        
        if auth_header is not None and len(auth_header.split(" ")) == 2:
            access_token = auth_header.split(" ")[1]
            user_id = User.decode_token(access_token)
            if isinstance(user_id, int):
        
                token_verify = User.query.filter_by(id=user_id).filter_by(token=access_token).first()
                if token_verify:
                    shoppinglist = ShoppingList.query.filter_by(id=list_id).first()
                    if not shoppinglist:
                        response = {'message': 'List Does Not Exist'}
                        return make_response(jsonify(response)), 404
                
                    if request.method == "POST":
                            
                        name = str(request.data.get('name', ''))

                        if name:
                            
                            listitem = ListItem(name=name, list_id=list_id)
                            ListItem.save(listitem)
                            response = jsonify({
                                'Id': listitem.id,
                                'Name': listitem.name,
                                'List': list_id
                            })
                            return make_response(response), 201
                        else:
                            return make_response(jsonify({"message": "Please Enter Some Valid Content"})), 400

                    elif request.method == "GET":

                        listitem_get = ListItem.query.filter_by(list_id=list_id)
                        results = []

                        for listitem in listitem_get:
                            list_data = {}
                            list_data['Id'] = listitem.id
                            list_data['Name'] = listitem.name
                            list_data['List'] = list_id
                            list_data['Owner'] = user_id
                            results.append(list_data)

                        return make_response(jsonify(results)), 200
                else:
                    response = {'message': 'Token is unusable - login again'}
                    return make_response(jsonify(response)), 401
            else:
                response = {'message': 'Token is Invalid'}
                return make_response(jsonify(response)), 401

        else:
            response = {'message': 'No Token Provided'}
            return make_response(jsonify(response)), 401   

    @app.route('/shoppinglists/<list_id>/items/<item_id>', methods=['GET', 'DELETE', 'PUT'])
    def item_modifications(item_id, **kwargs):
        
    
        auth_header = request.headers.get("Authorization")
        
        if auth_header is not None and len(auth_header.split(" ")) == 2:
            access_token = auth_header.split(" ")[1]
            user_id = User.decode_token(access_token)
            if isinstance(user_id, int):
        
                token_verify = User.query.filter_by(id=user_id).filter_by(token=access_token).first()
                if token_verify:
                    listitem = ListItem.query.filter_by(id=item_id).first()
                    if not listitem:
                        response = {'message': 'List Item Does Not Exist'}
                        return make_response(jsonify(response)), 404

                    if request.method == 'DELETE':
                        listitem.delete()
                        return {"message": "Item has been deleted"}

                    elif request.method == 'PUT':
                        name = str(request.data.get('name', ''))
                        listitem.name = name
                        listitem.save()

                        response = jsonify({
                        'id': listitem.id,
                        'name': listitem.name
                        })
                        return make_response(response), 200

                    elif request.method == 'GET':
                        response = jsonify({
                        'id': listitem.id,
                        'name':listitem.name
                        })
                        return make_response(response), 200
                else:
                    response = {'message': 'Token is unusable - login again'}
                    return make_response(jsonify(response)), 401
            else:
                response = {'message': 'Token is Invalid'}
                return make_response(jsonify(response)), 401

        else:
            response = {'message': 'No Token Provided'}
            return make_response(jsonify(response)), 401  




    from .auth import auth_blueprint
    app.register_blueprint(auth_blueprint)

    return app

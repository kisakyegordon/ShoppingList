from app import db
from flask_bcrypt import Bcrypt
from flask import current_app
import jwt
from datetime import datetime, timedelta

class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    country_town = db.Column(db.String(200), nullable=False)
    token = db.Column(db.String(300), nullable=True)
    lists = db.relationship("ShoppingList", order_by="ShoppingList.id", cascade="all, delete-orphan")


    def __init__(self, email, password, country_town, token=None):
        """Initialize the user with email and password"""

        self.email = email
        self.country_town = country_town
        self.token = token
        self.password = Bcrypt().generate_password_hash(password).decode()

    def password_is_valid(self, password):

        return Bcrypt().check_password_hash(self.password, password)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def generate_token(self, user_id):
        try:
            payload = {
                'exp' : datetime.utcnow() + timedelta(minutes=30),
                'iat' : datetime.utcnow(),
                'sub' : user_id
            }

            jwt_string = jwt.encode(
                payload,
                current_app.config.get('SECRET'),
                algorithm='HS256'
            )

            return jwt_string
        except Exception as e:
            return str(e)

    @staticmethod
    def decode_token(token):

        try:
            payload = jwt.decode(token, current_app.config.get('SECRET'))
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return "Expired token. Please login to get a new token"

        except jwt.InvalidTokenError:

            return "Invalid token. Please regidter or login"

class ShoppingList(db.Model):

    __tablename__ = 'shoppinglists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    owner = db.Column(db.Integer, db.ForeignKey(User.id))
    items = db.relationship("ListItem", order_by="ListItem.id", cascade="all, delete-orphan")


    def __init__(self, name):
        self.name = name


    def save(self):
        db.session.add(self)
        db.session.commit()


    # @staticmethod
    # def get_all():
    #     return ShoppingList.query.all()


    def delete(self):
        db.session.delete(self)
        db.session.commit()


    # def __repr__(self):
    #     return "<ShoppingList: {}>".format(self.name)



class ListItem(db.Model):
    
    __tablename__ = 'listitem'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(180))
    list_id = db.Column(db.Integer, db.ForeignKey(ShoppingList.id))

    def __init__(self, name):
        self.name = name

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return ListItem.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


        

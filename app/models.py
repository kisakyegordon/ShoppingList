from app import db
from flask_bcrypt import Bcrypt
from flask import current_app
import jwt
# import datetime
from datetime import datetime, timedelta




class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    lists = db.relationship("ShoppingList", order_by="ShoppingList.id", cascade="all, delete-orphan")


    def __init__(self, email, password):
        """Initialize the user with email and password"""

        self.email = email
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

    
    # def crush_token(self, user_id):
    #     try:
    #         payload = {
    #             'exp' : datetime.utcnow() + timedelta(minutes=0),
    #             'iat' : datetime.utcnow(),
    #             'sub' : user_id
    #         }

    #         jwt_string = jwt.encode(
    #             payload,
    #             current_app.config.get('SECRET'),
    #             algorithm='HS256'
    #         )
    #         return jwt_string
    #     except Exception as e:
    #         return str(e)

    @staticmethod
    def decode_token(token):

        try:
            payload = jwt.decode(token, current_app.config.get('SECRET'))
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return "Expired token. Please login to get a new token"

        except jwt.InvalidTokenError:

            return "Invalid token. Please regidter or login"

    # @staticmethod
    # def decode_token(token):
    #     """
    #     Validates the auth token
    #     """
    #     try:
    #         payload = jwt.decode(token, current_app.config.get('SECRET'))
    #         is_blacklisted_token = BlacklistToken.check_blacklist(token)
    #         if is_blacklisted_token:
    #             return 'Token blacklisted. Please log in again.'
    #         else:
    #             return payload['sub']
    #     except jwt.ExpiredSignatureError:
    #         return 'Signature expired. Please log in again.'
    #     except jwt.InvalidTokenError:
    #         return 'Invalid token. Please log in again.'


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


    @staticmethod
    def get_all():
        return ShoppingList.query.all()


    def delete(self):
        db.session.delete(self)
        db.session.commit()


    def __repr__(self):
        return "<ShoppingList: {}>".format(self.name)



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

class BlacklistToken(db.Model):
    """
    Model for storing blacklisted tokens
    """
    
    __tablename__ = 'blacklist'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(500), unique=True, nullable=False)
    blacklist_status = db.Column(db.Boolean, nullable=False)

    def __init__(self, token):
        self.token = token
        self.blacklist_status = True
        # self.blacklist_status = datetime.datetime.now()
        # self.blacklist_status = datetime.now()
    def __repr__(self):
        return '<id: token: {}'.format(self.token)

    def save(self):
        self.session.add(self)
        self.session.commit()

    @staticmethod
    def check_blacklist(auth_token):
        # check whether token has been blacklisted

        res = BlacklistToken.query.filter_by(token=str(auth_token)).first()
        if res:
            return True
        else:
            return False

        

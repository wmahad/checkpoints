from werkzeug import generate_password_hash, check_password_hash
from flask.ext.sqlalchemy import SQLAlchemy
from itsdangerous import(
    TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
# from flask.ext.api import FlaskAPI
from flask import Flask

import os
import datetime


app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])

secret_key = app.config.get('SECRET_KEY')

db = SQLAlchemy(app)


class User(db.Model):
    """ This class maps a user """
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    pwdhash = db.Column(db.String(150), nullable=False)
    bucket_lists = db.relationship(
        'BucketList', backref='bucketlist_', lazy='dynamic')

    def __init__(self, username, password):
        """Method is called when instantiation"""
        self.username = username
        self.set_password(password)

    def __repr__(self):
        """Method handles representation of the User Model"""
        return '{}'.format(self.id)

    def set_password(self, password):
        """Method used for encrypting a password"""
        self.pwdhash = generate_password_hash(password)

    def check_password(self, password):
        """Method used for checking sent and existing password"""
        return check_password_hash(self.pwdhash, password)

    def generate_auth_token(self, expiration=600):
        """Method used for generating authentication token"""
        s = Serializer(secret_key, expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        """Method used for verifying authentication token"""
        s = Serializer(secret_key)
        try:
            data = s.loads(token)
        except SignatureExpired:
            # Valid Token, but expired
            return None
        except BadSignature:
            # Invalid Token
            return None
        user_id = data['id']
        return user_id


class BucketList(db.Model):
    """ This class maps a bucket list """
    __tablename__ = 'bucketlist'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    date_created = db.Column(
        db.DateTime, default=datetime.datetime.now, nullable=False)
    date_modified = db.Column(
        db.DateTime, default=datetime.datetime.now, unique=True, nullable=False)
    created_by = db.Column(
        db.Integer, db.ForeignKey('user.id'), nullable=False)
    bucket_list_item = db.relationship(
        'BucketListItem', backref='bucket_listitem', lazy='dynamic')

    def __repr__(self):
        """Method used for representation of BucketList Model"""
        return '{}'.format(self.name)


class BucketListItem(db.Model):
    """ This class maps an item in a bucket list """
    __tablename__ = 'bucketlistitem'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    date_created = db.Column(
        db.DateTime, default=datetime.datetime.now, nullable=False)
    date_modified = db.Column(
        db.DateTime, default=datetime.datetime.now, nullable=False)
    done = db.Column(db.Boolean, default=False, nullable=False)
    b_id = db.Column(db.Integer, db.ForeignKey(
        'bucketlist.id'), nullable=False)

    def __init__(self, name, b_id):
        """Method used for instantiation of a BucketListItem Model"""
        self.name = name
        self.b_id = b_id

    def __repr__(self):
        """Method used for representation of a BucketListItem Model"""
        return '{}'.format(self.id)

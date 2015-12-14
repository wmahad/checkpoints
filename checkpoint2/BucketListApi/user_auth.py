from flask import g
from models import User
from flask.ext.httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(username, password):
    """Method used for verifying that username and password sent
    are the same as that stored in the database"""
    # Try to see if it's a token first
    user_id = User.verify_auth_token(username)
    if user_id:
        user = User.query.filter_by(id=user_id).one()
    else:
        user = User.query.filter_by(
            username=username).first()
        if not user or not user.check_password(password):
            return False
    g.user = user
    return True

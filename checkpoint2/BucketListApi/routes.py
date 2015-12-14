from flask import g, jsonify
from flask_restful import Resource, Api, reqparse, fields, marshal
from models import User, app, db
from user_auth import auth, verify_password
from apiviews.bucketlist import BucketLists, IndividualBucketLists
from apiviews.bucketlist_items import BucketListItems, ModifyBucketListItems


api = Api(app)


class SignUp(Resource):
    """A sign up view for letting us add user to the site"""

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('username', type=str, required=True,
                                 help='Username to create user', location='json')
        self.parser.add_argument('password', type=str, required=True,
                                 help='Password to create user', location='json')
        super(SignUp, self).__init__()

    def get(self):
        pass

    def post(self):
        try:
            # get a users username and password
            args = self.parser.parse_args()

            username = args['username']
            password = args['password']
        except Exception as e:
            return {'error': str(e)}, 400
        if password == '' or username == '':
            # if user name or password is empty return the error message
            return {'error': "please enter a username and password"}
        else:
            # otherwise query whether username
            # already exists in the database
            user = User.query.filter_by(username=username).first()
            if user is not None:
                # if username already exists in the database
                # then return an error message indicating
                # unavailability of the name
                return {'error': 'Username already exists'}
            else:
                # if not then store the user in the db
                # and then redirect to the login view
                try:
                    new_user = User(username=username, password=password)
                    db.session.add(new_user)
                    db.session.commit()
                    return {'success': 'User has been created'}, 201
                except Exception as e:
                    return {'error': 'Failed to create User'}


class Login(Resource):
    """Login view to let users login"""

    decorators = [auth.login_required]

    def post(self):
        token = g.user.generate_auth_token()
        return jsonify({'token': token.decode('ascii')})


class LogOut(Resource):

    def post(self):
        # when user logs out redirect the user to the index page
        pass


api.add_resource(SignUp, '/signup', '/signup/', endpoint='signup')
api.add_resource(LogOut, '/logout', '/auth/logout',
                 '/logout/', '/auth/logout/', endpoint='logout')
api.add_resource(Login, '/login', '/auth/login', '/login/',
                 '/auth/login/', endpoint='login')
api.add_resource(BucketLists, '/bucketlists',
                 '/bucketlists/', endpoint='bucketlist')
api.add_resource(IndividualBucketLists, '/bucketlists/<int:id>',
                 endpoint='single_bucketlist')
api.add_resource(BucketListItems, '/bucketlists/<int:id>/items', '/bucketlists/<int:id>/items/',
                 endpoint='bucketlist_item')
api.add_resource(ModifyBucketListItems, '/bucketlists/<int:id>/items/<int:item_id>', '/bucketlists/<int:id>/items/<int:item_id>/',
                 endpoint='list_item')


if __name__ == '__main__':
    app.run(debug=True)

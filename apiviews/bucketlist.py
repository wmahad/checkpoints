from flask import request, g, jsonify
from flask_restful import Resource, reqparse
from models import BucketList, db, app
import datetime
from user_auth import auth, verify_password


def make_single_public(item):
    """Method to make BucketList items json compatible"""
    output = []

    bucketlists = {}
    bucketlists['id'] = item.id
    bucketlists['name'] = item.name
    bucketlists['date_created'] = item.date_created
    bucketlists['date_modified'] = item.date_modified
    bucketlists['created_by'] = item.created_by
    buck_items = item.bucket_list_item.all()

    bucketlists['items'] = []

    for i in buck_items:
        bucks = {}
        bucks['name'] = i.name
        bucks['id'] = i.id
        bucks['done'] = i.done
        bucks['date_created'] = i.date_created
        bucks['date_modified'] = i.date_modified
        bucketlists['items'].append(bucks)
        del bucks
    output.append(bucketlists)
    del bucketlists

    return output


def make_public(arg):
    """Method to make BucketList item json compatible"""
    output = []

    for item in arg:
        bucketlists = {}
        bucketlists['id'] = item.id
        bucketlists['name'] = item.name
        bucketlists['date_created'] = item.date_created
        bucketlists['date_modified'] = item.date_modified
        bucketlists['created_by'] = item.created_by
        buck_items = item.bucket_list_item.all()

        bucketlists['items'] = []

        for i in buck_items:
            bucks = {}
            bucks['name'] = i.name
            bucks['id'] = i.id
            bucks['done'] = i.done
            bucks['date_created'] = i.date_created
            bucks['date_modified'] = i.date_modified
            bucketlists['items'].append(bucks)
            del bucks
        output.append(bucketlists)
        del bucketlists

    return output


class BucketLists(Resource):
    """Class that handles all route requests for a BucketList"""
    # Bucket list view
    decorators = [auth.login_required]

    def __init__(self):
        """Instantiate route request parameters"""
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('bucket_list_name', type=str, required=True,
                                 help='Enter bucket list name', location='json')
        super(BucketLists, self).__init__()

    def get(self):
        """Method to handle all get requests to the route"""
        # get limit of returned bucketlists
        # get name to search for bucketlist
        limit = request.args.get('limit')
        query_param = request.args.get('q')
        page_limit = app.config.get('ITEMS_PER_PAGE')
        # check for whether limit or query_param is None
        if limit is None and query_param is None:
            # if so get bucket lists where default pagination is 20
            get_bucket_lists = BucketList.query.filter_by(
                created_by=g.user.id).paginate(1, page_limit, False).items
            # if someone specifies the limit
        elif limit is not None:
            try:
                # try to convert it to an integer
                _limit = int(limit)
            except ValueError:
                # When it fails to convert return an error
                return {'error': "Can not convert to int. Please Check your URL"}
            # if entered limit is greater than default page limit
            # then change page limit otherwise leave it at default(20)
            if _limit > page_limit:
                page_limit = _limit
            # Query for bucket lists with whatever pagination
            get_bucket_lists = BucketList.query.filter_by(
                created_by=g.user.id).paginate(1, page_limit, False).items
        # if someone specifies query_parameter
        elif query_param is not None:
            get_bucket_lists = BucketList.query.filter_by(
                created_by=g.user.id, name=query_param
            ).paginate(1, page_limit, False).items.all()

        if get_bucket_lists:
            resp = jsonify({'BucketLists': make_public(get_bucket_lists)})
            return resp
        else:
            return {'message': "There are no bucket lists"}, 203

    def post(self):
        """Method to handle all post requests to the route"""
        # if the request method is post
        # recieve bucket list name
        # check whether bucket list with that
        # name and belongs to user
        try:
            # get a users username and password
            args = self.parser.parse_args()
            bucket_list_name = args['bucket_list_name']
        except Exception as e:
            return {'error': str(e)}, 400
        if bucket_list_name == '' or bucket_list_name is None or not bucket_list_name:
            # if bucket_list_name is empty return the error message
            # import ipdb
            # ipdb.set_trace()
            return {"error": "please enter a bucketlist"}, 203
        check_bucket_list = BucketList.query.filter_by(
            name=bucket_list_name, created_by=g.user.id).first()

        if check_bucket_list and check_bucket_list is not None:
            # if this bucket list does actually exist
            # display a message to the user
            return {'message': "bucket list : {} already exists".format(bucket_list_name)}, 203
        else:
            # otherwise create a new bucket list
            # and refresh the view
            new_bucket_list = BucketList(
                name=bucket_list_name, created_by=g.user.id)
            db.session.add(new_bucket_list)
            db.session.commit()
            return {'message': 'BucketList {} has been created'.format(bucket_list_name)}, 201


class IndividualBucketLists(Resource):
    """Class to handle all route requests for an Individual BucketList"""

    decorators = [auth.login_required]

    def __init__(self):
        """Instantiate route request parameters"""
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('bucket_list_name', type=str,
                                 help='Enter bucket list name', location='json')
        super(IndividualBucketLists, self).__init__()

    def get(self, id):
        """Method to handle all get requests to the route"""
        get_bucket_list = BucketList.query.filter_by(
            id=id, created_by=g.user.id).first()

        if get_bucket_list and get_bucket_list is not None:

            resp = jsonify(
                {'bucketlists': make_single_public(get_bucket_list)})
            return resp
        else:
            return {'error': 'Bucket list with id: {} does not exit'.format(id)}, 203

    def put(self, id):
        """Method to handle all put requests to the route"""
        try:
            args = self.parser.parse_args()

            name = args['bucket_list_name']
        except Exception as e:
            return {'error': str(e)}, 400

        if name == '' or name is None:
            return {'error': 'Enter a name please'}, 203

        update_bucket_list = BucketList.query.filter_by(
            id=id, created_by=g.user.id).first()

        if update_bucket_list and update_bucket_list is not None:
            update_bucket_list.name = name
            update_bucket_list.date_updated = datetime.datetime.now()
            db.session.commit()
            return {'message': "Successfully updated the bucket list: {}".format(name)}

    def delete(self, id):
        """Method to handle all delete requests to the route"""
        delete_bucket_list = BucketList.query.filter_by(
            id=id, created_by=g.user.id).first()
        name = delete_bucket_list.name
        if delete_bucket_list and delete_bucket_list is not None:
            db.session.delete(delete_bucket_list)
            db.session.commit()
            return {'message': "Successfully deleted the bucket list: {}".format(name)}

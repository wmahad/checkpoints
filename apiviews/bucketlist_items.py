from flask_restful import Resource, reqparse, marshal, fields
from models import BucketListItem, db
import datetime
from user_auth import auth, verify_password

items_fields = {
    'id': fields.String,
    'name': fields.String,
    'done': fields.Boolean,
    'date_created': fields.DateTime,
    'date_modified': fields.DateTime
}


class BucketListItems(Resource):
    """Class to handle all route requests for BucketList Items"""

    decorators = [auth.login_required]

    def __init__(self):
        """Instantiate route request parameters"""
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('item_name', type=str, required=True,
                                 help='Enter items name', location='json')
        super(BucketListItems, self).__init__()

    def get(self, id):
        """Method to handle all get requests to the route"""
        get_bucket_list_items = BucketListItem.query.filter_by(b_id=id).all()
        if get_bucket_list_items:
            return {'items': [marshal(item, items_fields) for item in get_bucket_list_items]}, 200
        return {"message": "there are no items under this bucket list"}, 203

    def post(self, id):
        """Method to handle all post requests to the route"""
        try:
            args = self.parser.parse_args()

            name = args['item_name']
        except Exception as e:
            return {'error': str(e)}, 400

        if name == '' or name is None:
            return {'error': 'Please enter a name'}, 203
        check_if_bucket_list_item_exists = BucketListItem.query.filter_by(
            name=name, b_id=id).first()
        if check_if_bucket_list_item_exists and check_if_bucket_list_item_exists is not None:
            return {'error': "{} already exists".format(name)}, 203
        else:
            new_bucket_list_item = BucketListItem(name=name, b_id=id)
            db.session.add(new_bucket_list_item)
            db.session.commit()
            return {'message': "{} Successfully created".format(name)}, 201


class ModifyBucketListItems(Resource):
    """Class to handle all route requests for Individual BucketList Item"""

    def __init__(self):
        """Instantiate route request parameters"""
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('item_name', type=str,
                                 help='Enter item name', location='json')
        self.parser.add_argument('done', type=bool, location='json')
        super(ModifyBucketListItems, self).__init__()

    decorators = [auth.login_required]

    def get(self, id, item_id):
        """Method to handle all get requests to the route"""
        get_bucket_list_item = BucketListItem.query.filter_by(
            id=item_id, b_id=id).all()
        if get_bucket_list_item:
            return {'item': marshal(get_bucket_list_item, items_fields)}, 200
        return {'message': "Item with id: {} doesn't exist".format(item_id)}, 203

    def put(self, id, item_id):
        """Method to handle all put requests to the route"""
        check_bucket_list_item_exists = BucketListItem.query.filter_by(
            id=item_id, b_id=id).first()
        try:
            args = self.parser.parse_args()
            name = args['item_name']
            done = args['done']
        except Exception as e:
            return {'error': str(e)}
        finished = False
        if done is None:
            finished = False

        if check_bucket_list_item_exists and check_bucket_list_item_exists is not None:
            check_bucket_list_item_exists.date_modified = datetime.datetime.now()
            if name and not name.isspace() and name is not None:
                check_bucket_list_item_exists.name = name

            check_bucket_list_item_exists.done = finished
            db.session.commit()
            return {'message': "{} updated Successfully".format(check_bucket_list_item_exists.name)}, 201

    def delete(self, id, item_id):
        """Method to handle all delete requests to the route"""
        delete_bucket_list_item = BucketListItem.query.filter_by(
            b_id=id, id=item_id).first()
        name = delete_bucket_list_item.name
        if delete_bucket_list_item and delete_bucket_list_item is not None:
            db.session.delete(delete_bucket_list_item)
            db.session.commit()
            return {'message': "Successfully deleted the bucket list item: {}".format(name)}

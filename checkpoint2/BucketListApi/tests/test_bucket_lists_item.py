from flask import url_for
import json
from test_base import BaseTestCase
from routes import db
from models import BucketListItem, User


class BucketListItemTests(BaseTestCase):
    """This class contains all tests for actions on a bucketlist_item"""

    def test_bucket_list_item_creation_suceeds_when_right_info_is_provided(self):
        """tests that creation of a bucket-list-item succeeds 
        when correct info is sent"""
        user = User(username='Joe', password='12345')
        db.session.add(user)
        db.session.commit()
        response = self.request(
            'POST', url_for('bucketlist_item', id=1), auth=('Joe', '12345'),
            data=json.dumps(
                {'item_name': 'Touch the sky'}),
            content_type='application/json')

        self.assertEqual(response.status_code, 201)
        self.assertIn(
            "Touch the sky Successfully created", response.data)

    def test_bucket_list_item_creation_fails_when_no_info_is_provided(self):
        """tests that creation of a bucket-list-item fails 
        when no info is sent"""
        user = User(username='Joe', password='12345')
        db.session.add(user)
        db.session.commit()
        response = self.request(
            'POST', url_for('bucketlist_item',  id=1), auth=('Joe', '12345'),
            data=json.dumps(
                {'item_name': ''}),
            content_type='application/json')
        self.assertEqual(response.status_code, 203)
        self.assertIn("Please enter a name", response.data)

    def test_bucket_list_item_creation_fails_when_same_item_is_provided(self):
        """tests that creation of a bucket-list-item fails 
        when same info is sent"""
        user = User(username='Joe', password='12345')
        db.session.add(user)
        db.session.commit()
        item = BucketListItem(name="Touch the sky", b_id=1)
        db.session.add(item)
        db.session.commit()
        response = self.request(
            'POST', url_for('bucketlist_item',  id=1), auth=('Joe', '12345'),
            data=json.dumps(
                {'item_name': 'Touch the sky'}),
            content_type='application/json')
        self.assertEqual(response.status_code, 203)
        self.assertIn(
            "Touch the sky already exists", response.data)

    def test_bucket_list_item_creation_fails_when_no_data_is_self(self):
        """tests that creation of a bucket-list-item fails 
        when no info is sent"""
        user = User(username='Joe', password='12345')
        db.session.add(user)
        db.session.commit()
        item = BucketListItem(name="Touch the sky", b_id=1)
        db.session.add(item)
        db.session.commit()
        response = self.request(
            'POST', url_for('bucketlist_item',  id=1), auth=('Joe', '12345'))
        self.assertEqual(response.status_code, 400)
        self.assertIn(
            "Bad Request", response.data)

    def test_existance_of_bucket_lists_items(self):
        """tests that there exists a bucket-list-item """
        user = User(username='Joe', password='12345')
        db.session.add(user)
        db.session.commit()
        item = BucketListItem(name="Touch the sky", b_id=1)
        db.session.add(item)
        db.session.commit()
        response = self.request(
            'GET', url_for('bucketlist_item', id=1), auth=('Joe', '12345'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            item.name, response.data)

    def test_existance_of_no_bucket_lists_items(self):
        """tests that there exists no bucket-list-item """
        user = User(username='Joe', password='12345')
        db.session.add(user)
        db.session.commit()
        response = self.request(
            'GET', url_for('bucketlist_item', id=1), auth=('Joe', '12345'))
        self.assertEqual(response.status_code, 203)
        self.assertIn(
            'there are no items under this bucket list', response.data)

    # # get for individual bucket lists
    def test_existance_of_single_bucket_list_item(self):
        """tests that there exists a single bucket-list-item """
        user = User(username='Joe', password='12345')
        db.session.add(user)
        db.session.commit()
        item = BucketListItem(name="Touch the sky", b_id=1)
        db.session.add(item)
        db.session.commit()
        response = self.request(
            'GET', url_for('list_item', id=1, item_id=1), auth=('Joe', '12345'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            item.name, response.data)

    def test_existance_of_no_single_bucket_list_item(self):
        """tests that there exists no single bucket-list-item """
        user = User(username='Joe', password='12345')
        db.session.add(user)
        db.session.commit()
        response = self.request(
            'GET', url_for('list_item', id=1, item_id=1), auth=('Joe', '12345'))
        self.assertEqual(response.status_code, 203)
        self.assertIn(
            "Item with id: 1 doesn't exist", response.data)

    # # Update method for the bucket list

    def test_update_of_single_bucket_list_item_succeeds(self):
        """tests that update of a bucket-list-item succeeds 
        when right is sent"""
        user = User(username='Joe', password='12345')
        db.session.add(user)
        db.session.commit()
        item = BucketListItem(name="Bucket List 1", b_id=1)
        db.session.add(item)
        db.session.commit()
        response = self.request(
            'PUT', url_for('list_item', id=1, item_id=1), auth=('Joe', '12345'),
            data=json.dumps(
                {'item_name': 'Touch the sky', 'done': True}),
            content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIn(
            "Touch the sky updated Successfully", response.data)

    def test_deletion_of_single_bucket_list_item_succeds(self):
        """tests that deletion of a bucket-list-item succeeds"""
        user = User(username='Joe', password='12345')
        db.session.add(user)
        db.session.commit()
        item = BucketListItem(name="Touch the sky", b_id=1)
        db.session.add(item)
        db.session.commit()
        response = self.request(
            'DELETE', url_for('list_item', id=1, item_id=1), auth=('Joe', '12345'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            "Successfully deleted the bucket list item: {}".format(item.name), response.data)

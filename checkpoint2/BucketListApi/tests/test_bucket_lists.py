from flask import url_for
import json
from test_base import BaseTestCase
from routes import db
from models import BucketList, User


class BucketListTests(BaseTestCase):
    """This class contains all tests for a bucketlist"""

    def test_bucket_list_creation_suceeds_when_right_info_is_provided(self):
        """tests that creation of a bucket-list succeeds when correct info is sent"""
        user = User(username='Joe', password='12345')
        db.session.add(user)
        db.session.commit()
        response = self.request(
            'POST', url_for('bucketlist'), auth=('Joe', '12345'),
            data=json.dumps(
                {'bucket_list_name': 'Bucket List 1'}),
            content_type='application/json')

        self.assertEqual(response.status_code, 201)
        self.assertIn(
            "BucketList Bucket List 1 has been created", response.data)

    def test_bucket_list_creation_fails_when_no_info_is_provided(self):
        """tests that creation of a bucket-list fails when wrong info is sent"""
        user = User(username='Joe', password='12345')
        db.session.add(user)
        db.session.commit()
        response = self.request(
            'POST', url_for('bucketlist'), auth=('Joe', '12345'),
            data=json.dumps(
                {'bucket_list_name': ''}),
            content_type='application/json')
        self.assertEqual(response.status_code, 203)
        self.assertIn("please enter a bucketlist", response.data)

    def test_bucket_list_creation_fails_when_same_bucket_list_is_provided(self):
        """tests that creation of a bucket-list fails when same info is sent"""
        user = User(username='Joe', password='12345')
        db.session.add(user)
        db.session.commit()
        bucketlist = BucketList(name="Bucket List 1", created_by=user.id)
        db.session.add(bucketlist)
        db.session.commit()
        response = self.request(
            'POST', url_for('bucketlist'), auth=('Joe', '12345'),
            data=json.dumps(
                {'bucket_list_name': 'Bucket List 1'}),
            content_type='application/json')
        self.assertEqual(response.status_code, 203)
        self.assertIn(
            "bucket list : Bucket List 1 already exists", response.data)

    def test_existance_of_bucket_lists(self):
        """tests that there exists bucket-lists"""
        user = User(username='Joe', password='12345')
        db.session.add(user)
        db.session.commit()
        bucketlist = BucketList(name="Bucket List 1", created_by=user.id)
        db.session.add(bucketlist)
        db.session.commit()
        response = self.request(
            'GET', url_for('bucketlist'), auth=('Joe', '12345'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            bucketlist.name, response.data)

    def test_existance_of_no_bucket_lists(self):
        """tests that there are no bucket-lists"""
        user = User(username='Joe', password='12345')
        db.session.add(user)
        db.session.commit()
        response = self.request(
            'GET', url_for('bucketlist'), auth=('Joe', '12345'))
        self.assertEqual(response.status_code, 203)
        self.assertIn(
            'There are no bucket lists', response.data)

    # get for individual bucket lists
    def test_existance_of_single_bucket_list(self):
        """tests that there exists a single bucket-list"""
        user = User(username='Joe', password='12345')
        db.session.add(user)
        db.session.commit()
        bucketlist = BucketList(name="Bucket List 1", created_by=user.id)
        db.session.add(bucketlist)
        db.session.commit()
        response = self.request(
            'GET', url_for('single_bucketlist', id=1), auth=('Joe', '12345'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            bucketlist.name, response.data)

    def test_existance_of_no_single_bucket_lists(self):
        """tests that there exists no single bucket-list"""
        user = User(username='Joe', password='12345')
        db.session.add(user)
        db.session.commit()
        response = self.request(
            'GET', url_for('single_bucketlist', id=1), auth=('Joe', '12345'))
        self.assertEqual(response.status_code, 203)
        self.assertIn(
            'Bucket list with id: 1 does not exit', response.data)

    # Update method for the bucket list

    def test_update_of_single_bucket_list_succeeds(self):
        """tests that updating a bucket list succeeds when
        right info is sent"""
        user = User(username='Joe', password='12345')
        db.session.add(user)
        db.session.commit()
        bucketlist = BucketList(name="Bucket List 1", created_by=user.id)
        db.session.add(bucketlist)
        db.session.commit()
        response = self.request(
            'PUT', url_for('single_bucketlist', id=1), auth=('Joe', '12345'),
            data=json.dumps(
                {'bucket_list_name': 'Bucket List One'}),
            content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            "Successfully updated the bucket list: Bucket List One", response.data)

    def test_update_of_single_bucket_list_fails_when_no_info_is_provide(self):
        """tests that update of a bucket-list fails when no info is sent"""
        user = User(username='Joe', password='12345')
        db.session.add(user)
        db.session.commit()
        bucketlist = BucketList(name="Bucket List 1", created_by=user.id)
        db.session.add(bucketlist)
        db.session.commit()
        response = self.request(
            'PUT', url_for('single_bucketlist', id=1), auth=('Joe', '12345'),
            data=json.dumps(
                {'bucket_list_name': ''}),
            content_type='application/json')
        self.assertEqual(response.status_code, 203)
        self.assertIn(
            "Enter a name please", response.data)

    def test_update_of_single_bucket_list_fails_when_user_is_not_authenticated(self):
        """tests that update of a bucket-list fails when user is no authenticated"""
        user = User(username='Joe', password='12345')
        db.session.add(user)
        db.session.commit()
        bucketlist = BucketList(name="Bucket List 1", created_by=user.id)
        db.session.add(bucketlist)
        db.session.commit()
        response = self.request(
            'PUT', url_for('single_bucketlist', id=1), auth=('Joel', '12345'))
        self.assertEqual(response.status_code, 401)
        self.assertIn(
            "Unauthorized Access", response.data)

    def test_deletion_of_single_bucket_list_succeds(self):
        """tests that delete of a bucket-list succeeds"""
        user = User(username='Joe', password='12345')
        db.session.add(user)
        db.session.commit()
        bucketlist = BucketList(name="Bucket List 1", created_by=user.id)
        db.session.add(bucketlist)
        db.session.commit()
        response = self.request(
            'DELETE', url_for('single_bucketlist', id=1), auth=('Joe', '12345'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            "Successfully deleted the bucket list: {}".format(bucketlist.name), response.data)

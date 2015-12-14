from flask import url_for
import json
from test_base import BaseTestCase
from routes import db
from models import User
from user_auth import auth, verify_password


class SignUpViewTests(BaseTestCase):

    def test_users_can_sign_up_when_they_provide_correct_info(self):
        response = self.client.post(url_for('signup'),
                                    data=json.dumps({'username': 'Joe',
                                                     'password': '12345'}), content_type='application/json')
        self.assertIn('User has been created', response.data)
        self.assertEqual(response.status_code, 201)

    def test_users_can_not_sign_up_when_they_provide_wrong_info(self):
        response = self.client.post(url_for('signup'),
                                    data=json.dumps({'password': '12345'}), content_type='application/json')
        self.assertIn("Bad Request", response.data)
        self.assertEqual(response.status_code, 400)

    def test_users_can_not_sign_up_when_they_provide_existing_info(self):
        user = User(username='Joe', password='12345')
        db.session.add(user)
        db.session.commit()
        response = self.client.post(url_for('signup'),
                                    data=json.dumps({'username': 'Joe', 'password': '12345'}), content_type='application/json')
        self.assertIn("Username already exists", response.data)
        self.assertEqual(response.status_code, 200)

    def test_users_can_not_sign_up_when_they_provide_no_info(self):
        response = self.client.post(url_for('signup'),
                                    data=json.dumps({'username': '', 'password': ''}), content_type='application/json')
        self.assertIn("please enter a username and password", response.data)
        self.assertEqual(response.status_code, 200)


# class LogOutViewTests(BaseTestCase):

#     def test_users_can_log_out(self):
#         response = self.client.get(url_for('logout'))
#         self.assert_redirects(response, url_for('index'))


class LoginViewTests(BaseTestCase):

    def test_users_can_not_sign_in_when_they_provide_wrong_info(self):
        user = User(username='Joe', password='12345')
        db.session.add(user)
        db.session.commit()
        response = self.request('POST', url_for(
            'login'), auth=('Joel', '12345'))
        self.assertIn("Unauthorized Access", response.data)
        self.assertEqual(response.status_code, 401)

    def test_users_can_not_sign_in_when_they_provide_no_info(self):
        response = self.request('POST', url_for(
            'login'), auth=('', ''))
        self.assertIn("Unauthorized Access", response.data)
        self.assertEqual(response.status_code, 401)

    def test_users_can_sign_in_when_they_provide_right_info(self):
        user = User(username='Joe', password='12345')
        db.session.add(user)
        db.session.commit()
        response = self.request('POST', url_for(
            'login'), auth=('Joe', '12345'))
        self.assertNotIn("Unauthorized Access", response.data)
        self.assertIn("token", response.data)
        self.assertEqual(response.status_code, 200)

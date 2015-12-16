from flask.ext.testing import TestCase

from routes import app, db
import base64


class BaseTestCase(TestCase):
    """A base test case for flask-tracking."""

    def create_app(self):
        """method for setting up config variables for the app"""
        app.config.from_object('config.TestingConfig')
        return app

    def setUp(self):
        """setUp method"""
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        """method for clearing all settings"""
        db.session.remove()
        db.drop_all()

    def request(self, method, url, auth=None, **kwargs):
        """method to use to represent Authorization means for the tests"""
        headers = kwargs.get('headers', {})
        if auth:
            headers['Authorization'] = 'Basic ' + \
                base64.b64encode(auth[0] + ':' + auth[1])

        kwargs['headers'] = headers

        return self.app.open(url, method=method, **kwargs)

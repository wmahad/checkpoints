from flask.ext.testing import TestCase

from routes import app, db
import base64


class BaseTestCase(TestCase):
    """A base test case for flask-tracking."""

    def create_app(self):
        app.config.from_object('config.TestingConfig')
        return app

    def setUp(self):
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def request(self, method, url, auth=None, **kwargs):
        headers = kwargs.get('headers', {})
        if auth:
            headers['Authorization'] = 'Basic ' + \
                base64.b64encode(auth[0] + ':' + auth[1])

        kwargs['headers'] = headers

        return self.app.open(url, method=method, **kwargs)

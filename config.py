import os
import random
import string


class Config(object):
    """A class to contain app wide configurations"""
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = ''.join(random.choice(
        string.ascii_uppercase + string.digits) for x in xrange(32))
    ITEMS_PER_PAGE = 20
    if os.getenv('TRAVIS_BUILD', None):
        SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    else:
        SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']


class ProductionConfig(Config):
    """A class to contain production configurations"""
    DEBUG = False


class StagingConfig(Config):
    """A class to contain staging configurations"""
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    """A class to contain Development configurations"""
    DEVELOPMENT = False
    DEBUG = False


class TestingConfig(Config):
    """A class to contain testing configurations"""
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    # Since we want our unit tests to run quickly
    # we turn this down - the hashing is still done
    # but the time-consuming part is left out.
    HASH_ROUNDS = 1

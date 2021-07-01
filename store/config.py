import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestConfig(object):
    # Enable the TESTING flag to disable the error catching during request handling
    # so that you get better error reports when performing test requests against the application.
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite://"

    DATABASE = ''

    SQLALCHEMY_TRACK_MODIFICATIONS = False

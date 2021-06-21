import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://postgres:postgres@0.0.0.0:5432/yandex_store'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

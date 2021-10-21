from dotenv import load_dotenv
import os

DEFAULT_URL_VALIDATOR = 'https://n1.pnrd.net:8008'
DEFAULT_URL_SAWTOOH_REST_API = 'https://n1.pnrd.net:8008'
AES_KEY = 'ffffffffffffffffffffffffffffffff'
APP_SECRET_KEY = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'


class Config(object):
    DEBUG = False
    TESTING = False


class CoreConfig(Config):
    ENV = "ENV-BETA"
    DEBUG = True
    JSON_SORT_KEYS = False


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = ""
    SQLALCHEMY_ECHO = False

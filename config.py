import os
from os.path import dirname, join
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
secret_key = os.urandom(24)


class Config(object):
    BASE_DIR = dirname(__file__)
    DEBUG = False
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PAGE_LIMIT = 10
    DEFAULT_PAGE = 1

    # Secret key for signing cookies
    SECRET_KEY = os.getenv('SECRET_KEY', secret_key)

    # email server
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')


class ConfigWithCustomDBEngineParams(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    try:
        SQLALCHEMY_POOL_SIZE, SQLALCHEMY_MAX_OVERFLOW, SQLALCHEMY_POOL_TIMEOUT\
            = int(os.environ.get('SQLALCHEMY_POOL_SIZE')),\
            int(os.environ.get('SQLALCHEMY_MAX_OVERFLOW')),\
            int(os.environ.get('SQLALCHEMY_POOL_TIMEOUT'))
    except (TypeError, ValueError):
        SQLALCHEMY_POOL_SIZE, SQLALCHEMY_POOL_SIZE, SQLALCHEMY_POOL_SIZE =\
            5, 10, 30


class DevelopmentConfiguration(ConfigWithCustomDBEngineParams):
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
    DEBUG = True
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class TestingConfiguration(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + Config.BASE_DIR \
                              + "/test/test_db.sqlite"
    PAGE_LIMIT = 2


app_configuration = {
    'production': ConfigWithCustomDBEngineParams,
    'development': DevelopmentConfiguration,
    'testing': TestingConfiguration
}

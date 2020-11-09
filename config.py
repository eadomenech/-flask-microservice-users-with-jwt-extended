from dotenv import load_dotenv
import os


# parse .env file if exists
load_dotenv()


class BaseConfig(object):
    """Base configuration"""
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SECRET_KEY = os.environ.get('SECRET_KEY')
    APIFAIRY_TITLE = 'Users API'
    APIFAIRY_VERSION = '1.0'
    APIFAIRY_UI_PATH = '/'
    BCRYPT_LOG_ROUNDS = 4
    TOKEN_EXPIRATION_DAYS = 30
    TOKEN_EXPIRATION_SECONDS = 0

    JWT_ALGORITHM='RS256'
    JWT_SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret-key'
    JWT_PRIVATE_KEY = open('private/jwt-key').read()
    JWT_PUBLIC_KEY = open('private/jwt-key.pub').read()

    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.example.com'
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') or 1
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'user@example.com'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'password'
    ADMINS = os.environ.get('ADMINS') or ['support@example.com']


class DevelopmentConfig(BaseConfig):
    """Development configuration"""
    ENV = 'development'
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_DEV_URL')


class TestingConfig(BaseConfig):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_TEST_URL')
    TOKEN_EXPIRATION_DAYS = 0
    TOKEN_EXPIRATION_SECONDS = 3


class ProductionConfig(BaseConfig):
    """Production configuration"""
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    BCRYPT_LOG_ROUNDS = 13

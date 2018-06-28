import os
import psycopg2

base_dir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig:
    """
    Base application configuration
    """
    DEBUG = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'This_ismyStrongestSecretKeyMan')
    AUTH_TOKEN_EXPIRY_DAYS = 30
    AUTH_TOKEN_EXPIRY_SECONDS = 3000


class DevelopmentConfig(BaseConfig):
    """
    Development application configuration
    """
    DEBUG = True
    BCRYPT_HASH_PREFIX = 4
    AUTH_TOKEN_EXPIRY_DAYS = 1
    AUTH_TOKEN_EXPIRY_SECONDS = 20


class TestingConfig(BaseConfig):
    """
    Testing application configuration
    """
    DEBUG = True
    TESTING = True
    BCRYPT_HASH_PREFIX = 4
    AUTH_TOKEN_EXPIRY_DAYS = 0
    AUTH_TOKEN_EXPIRY_SECONDS = 3
    AUTH_TOKEN_EXPIRATION_TIME_DURING_TESTS = 5


class ProductionConfig(BaseConfig):
    """
    Production application configuration
    """
    DEBUG = True
    PRODUCTION = True
    BCRYPT_HASH_PREFIX = 13
    AUTH_TOKEN_EXPIRY_DAYS = 30
    AUTH_TOKEN_EXPIRY_SECONDS = 20

app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
}

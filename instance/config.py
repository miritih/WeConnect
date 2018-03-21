import os
class Config(object):
    """docstring for Config"""
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
class Development(Config):
    """docstring for Development"""
    DEBUG = True

class Testing(Config):
    """docstring for Testing"""
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "postgres:///weconnect_test"

class Production(Config):
    """"""
    DEBUG = False

app_config = {
    'development': Development,
    'testing': Testing,
    'production': Production,
}

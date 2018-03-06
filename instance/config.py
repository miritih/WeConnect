import os


class Config(object):
    """docstring for Config"""
    DEBUG = False
    SECRET = os.getenv('SECRET_KEY')


class Development(Config):
    """docstring for Development"""
    DEBUG = True


class Testing(Config):
    """docstring for Testing"""
    DEBUG = True
    TESTING = True


class Production(Config):
    """"""
    DEBUG = False
    TESTING = False

app_config = {
    'development': Development,
    'testing': Testing,
    'production': Production,
}

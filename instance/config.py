import os


class Config(object):
    """docstring for Config"""
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER='smtp.gmail.com'
    MAIL_PORT=465
    MAIL_USE_SSL=True
    MAIL_USERNAME = 'ericmwenda254@gmail.com'
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')

class Development(Config):
    """docstring for Development"""
    DEBUG = True


class Testing(Config):
    """docstring for Testing"""
    DEBUG = True
    MAIL_SUPPRESS_SEND= False
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

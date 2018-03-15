from flask import Flask, Blueprint
import os
from instance.config import app_config
from app.v1 import version1


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile('config.py')
    app.register_blueprint(version1, url_prefix="/api/v1/")
    return app

config_name = os.getenv('APP_SETTINGS')
app = create_app(config_name)

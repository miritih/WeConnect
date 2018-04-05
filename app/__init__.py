from flask import Flask, Blueprint
import os
from instance.config import app_config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.v1 import version1

db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.register_blueprint(version1, url_prefix="/api/v1/")
    from app.v2 import version2
    app.register_blueprint(version2, url_prefix="/api/v2/")
    # initialize extensions
    migrate = Migrate(app, db)
    db.init_app(app)
    return app

import app.models.v2
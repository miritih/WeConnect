from flask import Flask, Blueprint
import os
from instance.config import app_config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from app.v1.v1 import version1


db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    CORS(app) #makes cross-origin AJAX possible.
    app.config.from_object(app_config[config_name])
    CORS(app) #makes cross-origin AJAX possible.
    app.config.from_pyfile('config.py')
    app.register_blueprint(version1, url_prefix="/api/v1/")
    # import all bluprints and register.
    from app.v2.business import version2
    from app.v2.review import review
    from app.v2.auth import auth
    app.register_blueprint(version2, url_prefix="/api/v2/")
    app.register_blueprint(auth, url_prefix="/api/v2/")
    app.register_blueprint(review, url_prefix="/api/v2/")
    # initialize extensions
    migrate = Migrate(app, db)
    db.init_app(app)
    return app

import app.models.v2

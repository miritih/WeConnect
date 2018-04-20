from flask import Blueprint, render_template
import os
from app import create_app

home = Blueprint('home', __name__)

# create application istance and push it to app context
app = create_app(os.getenv('APP_SETTINGS'))
app.app_context().push()

@home.route('/')
def Home():
    return render_template('swagger.html')
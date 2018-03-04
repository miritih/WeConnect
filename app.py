from flask import Flask, jsonify, request, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from models import Model

# create a flask app instance
app = Flask(__name__)

# instance of model taht will store app data
# application will use data structures to srore data
db = Model()

# secrete key to be usd in encrypting app authentication token
app.config['SECRET_KEY'] = '73283782qwwerty@987654321'


@app.route('/api/auth/register', methods=['POST'])
def register():
    """
    Route to create user, it will receive data through a post method
    """
    pass


if __name__ == '__main__':
    app.run(debug=True)

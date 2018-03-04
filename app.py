from flask import Flask, jsonify, request, make_response, session
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
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
    """Route to create user, it will receive data through a post method"""
    data = request.get_json()  # get data from the api consumer
    hashed_password = generate_password_hash(data['password'], method='sha256')
    if data['username'] in db.get_all_users():  # test if username exists
        return jsonify({"message": "Sorry!! Username taken!"})
    db.add_user(data['username'], hashed_password,
                data['first_name'], data['last_name'])
    return jsonify({'message': 'User created!'}), 201


@app.route('/api/auth/login', methods=['POST'])
def login():
    """login route. users will login to the app via this route"""
    auth = request.get_json()
    if not auth or not auth['username'] or not auth['password']:
        return jsonify({"message": "login required!"}), 401
    if auth['username'] in db.get_all_users():
        user = db.get_all_users()[auth['username']]
    else:
        return jsonify({"message": "Username not found!"}), 401
    if check_password_hash(user['password'], auth['password']):
        token = jwt.encode(
            {'username': user['username']}, app.config['SECRET_KEY'])
        session['username'] = user['username']
        session['token'] = token
        return jsonify({"token": token.decode('UTF-8')}), 200
    return jsonify({"message": "login required!"}), 401

if __name__ == '__main__':
    app.run(debug=True)

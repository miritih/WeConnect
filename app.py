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
    """Route to create user, it will receive data through a post method"""
    data = request.get_json()  # get data from the api consumer
    hashed_password = generate_password_hash(data['password'], method='sha256')
    if data['username'] in db.get_all_users():  # test if username exists
        return jsonify({"message": "Sorry!! Username taken!"})
    db.add_user(data['username'], hashed_password,
                data['first_name'], data['last_name'])
    return jsonify({'message': 'User created!'}), 201

if __name__ == '__main__':
    app.run(debug=True)

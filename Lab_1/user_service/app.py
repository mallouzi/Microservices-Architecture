
from flask import Flask, request, jsonify

app = Flask(__name__)
users = []

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    users.append(data)
    return jsonify({'message': 'User registered'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    for user in users:
        if user['username'] == data['username'] and user['password'] == data['password']:
            return jsonify({'message': 'Login successful'}), 200
    return jsonify({'message': 'Invalid credentials'}), 401

if __name__ == '__main__':
    app.run(host='0.0.0.0' ,port=5001)

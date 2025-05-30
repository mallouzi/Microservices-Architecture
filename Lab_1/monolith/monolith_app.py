
from flask import Flask, request, jsonify

app = Flask(__name__)

users = []
products = []
orders = []

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data.get('username') or not data.get('password'):
        return jsonify({'error': 'Missing fields'}), 400
    users.append(data)
    return jsonify({'message': 'User registered'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    for user in users:
        if user['username'] == data['username'] and user['password'] == data['password']:
            return jsonify({'message': 'Login successful'}), 200
    return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/products', methods=['POST'])
def add_product():
    data = request.get_json()
    if not data.get('id') or not data.get('name'):
        return jsonify({'error': 'Missing fields'}), 400
    products.append(data)
    return jsonify({'message': 'Product added'}), 201

@app.route('/products', methods=['GET'])
def list_products():
    return jsonify(products), 200

@app.route('/order', methods=['POST'])
def place_order():
    data = request.get_json()
    if not data.get('product_id') or not data.get('username'):
        return jsonify({'error': 'Missing fields'}), 400
    
    product_found = any(p['id'] == data['product_id'] for p in products)
    user_found = any(u['username'] == data['username'] for u in users)
    
    if not product_found:
        return jsonify({'error': 'Product not found'}), 404
    if not user_found:
        return jsonify({'error': 'User not found'}), 404

    orders.append(data)
    return jsonify({'message': 'Order placed'}), 201

@app.route('/orders', methods=['GET'])
def get_orders():
    return jsonify(orders), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)

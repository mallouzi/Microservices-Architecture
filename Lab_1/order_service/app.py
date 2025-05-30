
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)
orders = []

@app.route('/order', methods=['POST'])
def place_order():
    data = request.get_json()
    product_id = data.get('product_id')

    try:
        resp = requests.get(f'http://product_service:5002/products')
        products = resp.json()
        product_exists = any(p['id'] == product_id for p in products)

        if not product_exists:
            return jsonify({'error': 'Product not found'}), 404

        orders.append(data)
        return jsonify({'message': 'Order placed'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/orders', methods=['GET'])
def get_orders():
    return jsonify(orders), 200

if __name__ == '__main__':
    app.run(port=5003)

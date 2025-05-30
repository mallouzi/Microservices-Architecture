
from flask import Flask, request, jsonify

app = Flask(__name__)
products = []

@app.route('/products', methods=['POST'])
def add_product():
    data = request.get_json()
    products.append(data)
    return jsonify({'message': 'Product added'}), 201

@app.route('/products', methods=['GET'])
def list_products():
    return jsonify(products), 200

if __name__ == '__main__':
    app.run(port=5002)

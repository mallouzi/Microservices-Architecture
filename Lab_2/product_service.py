from flask import Flask
app = Flask(__name__)
@app.route('/api/products')
def get_products():
    return {'products': ['Product A', 'Product B']}

if __name__ == '__main__':
    app.run(port=5001)
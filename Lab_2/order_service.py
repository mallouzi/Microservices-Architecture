from flask import Flask, request
app = Flask(__name__)
@app.route('/api/place', methods=['POST'])
def place_order():
    return {'message': 'Order placed successfully'}

if __name__ == '__main__':
    app.run(port=5002)
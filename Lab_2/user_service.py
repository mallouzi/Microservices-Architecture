from flask import Flask
app = Flask(__name__)
@app.route('/api/profile')
def user_profile():
    return {'user': 'test_user'}

if __name__ == '__main__':
    app.run(port=5003)
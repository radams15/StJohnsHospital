import os

from flask import *
from werkzeug.exceptions import BadRequestKeyError
import jwt
from dotenv import load_dotenv

from SSOManager import SSOManager
from UserDao import UserDao

app = Flask(__name__)

load_dotenv('../.env')

user_dao = UserDao("users.json")
sso_manager = SSOManager(user_dao)

secret = os.getenv('SECRET')


@app.route('/login', methods=['GET'])
def login_page():
    try:
        success_redirect = request.args['redirect']
    except BadRequestKeyError:
        return {
            'status': 'failure',
            'message': 'Login requires redirect path'
        }

    return render_template('login.html', success_redirect=success_redirect)


@app.route('/login', methods=['POST'])
def login_post():
    username, password, success_redirect = request.form['username'], request.form['password'], request.form['redirect']

    if not sso_manager.validate_user(username, password):
        return {
            'state': 'failure'
        }

    user = user_dao.get_user(username)

    payload = {
        'username': username,
        'roles': [x[1] for x in user_dao.user_roles(username)],
        'secret': user['secret']
    }

    payload_token = jwt.encode(payload, secret, algorithm='HS256')

    return redirect('?'.join((success_redirect, f'token={payload_token}')))


if __name__ == '__main__':
    app.run(port=1111, debug=True)

from flask import *
from werkzeug.exceptions import BadRequestKeyError
import jwt

from SSOManager import SSOManager
from UserDao import UserDao

app = Flask(__name__)

user_dao = UserDao("users.sqlite")
sso_manager = SSOManager(user_dao)

SECRET = 'a-very-long-secret-pls-dont-steal'


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

    payload = {
        'username': username,
        'roles': [x[0] for x in user_dao.user_roles(username)]
    }

    payload_token = jwt.encode(payload, SECRET, algorithm='HS256')

    return redirect('?'.join((success_redirect, payload_token)))


if __name__ == '__main__':
    app.run(port=1111)

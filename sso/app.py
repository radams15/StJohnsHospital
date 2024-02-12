import os
import uuid

from flask import *
from werkzeug.exceptions import BadRequestKeyError
import jwt
from dotenv import load_dotenv

from SSOManager import SSOManager
from UserDao import UserDao

app = Flask(__name__)
app.secret_key = uuid.uuid4().hex

load_dotenv('../.env')

secret = os.getenv('SECRET')

user_dao = UserDao("users.json", secret)
sso_manager = SSOManager(user_dao)


@app.route('/login', methods=['GET'])
def login_page():
    try:
        success_redirect = request.args['redirect']
    except BadRequestKeyError:
        return {
            'status': 'failure',
            'message': 'Login requires redirect path'
        }

    if token := request.cookies.get('authentication'):
        try:
            data = jwt.decode(token, secret, algorithms='HS256')
            print(data)
            return redirect('?'.join((success_redirect, f'token={token}')))
        except:
            pass


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

    resp = make_response(redirect('?'.join((success_redirect, f'token={payload_token}'))))
    resp.set_cookie('authentication', payload_token, max_age=600)
    return resp

@app.route('/logout', methods=['GET'])
def logout():
    resp = make_response(redirect('/')) # Delete the cookie
    resp.set_cookie('authentication', '', expires=0)
    return resp

@app.route('/')
def index():
    return make_response('<h1>SSO</h1>', 200)

if __name__ == '__main__':
    app.run(port=1111, debug=True)

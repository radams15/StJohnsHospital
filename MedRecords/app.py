import os
from functools import wraps

from flask import *
from dotenv import load_dotenv
import jwt

load_dotenv('../.env')

app = Flask(__name__)

secret = os.getenv('SECRET')
auth_addr = os.getenv('AUTH_ADDR')

app.secret_key = secret


def authorise(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        if 'authentication' in session.keys():
            auth = session['authentication']
            try:
                data = jwt.decode(auth, secret, algorithms='HS256')
            except Exception as e:
                print(e)
                return make_response({'status': 'failure', 'message': 'invalid authorisation token'})

            return f(data, *args, **kwargs)
        else:
            return redirect('?'.join((f'{auth_addr}/login', f'redirect=http://localhost:2222/callback')))

    return decorator


@app.route('/callback')
def callback():
    tok = request.args.get('token')
    if tok:
        session['authentication'] = tok
        return redirect('/')
    else:
        return make_response({'status': 'failure', 'message': 'invalid authorisation token'})


@app.route('/')
@authorise
def index(data):
    return render_template('index.html', username=data['username'])


if __name__ == '__main__':
    app.run(port=2222, debug=True)

from functools import wraps
from flask import session, make_response, redirect
import jwt


def create_authorisation(secret, auth_addr, redirect_path):
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
                return redirect('?'.join((f'{auth_addr}/login', f'redirect={redirect_path}/callback')))

        return decorator
    return authorise

def logout(auth_addr):
    if 'authentication' in session:
        del session['authentication']
    return redirect(f'{auth_addr}/logout')

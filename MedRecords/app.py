import os
import sys
import uuid
from itertools import chain

from flask import *
from dotenv import load_dotenv

sys.path.append('../shared')

import Authorisation
from PatientDataDao import PatientDataDao


load_dotenv('../.env')

app = Flask(__name__)
app.secret_key = uuid.uuid4().hex

secret = os.getenv('SECRET')
auth_addr = os.getenv('AUTH_ADDR')

patient_data_dao = PatientDataDao('data.json', secret)

authorise = Authorisation.create_authorisation(secret, auth_addr, "https://localhost:2222")


@app.route('/callback')
def callback():
    tok = request.args.get('token')
    if tok:
        session['authentication'] = tok
        return redirect('/')
    else:
        return make_response({'status': 'failure', 'message': 'invalid authorisation token'})


@app.route('/all')
@authorise
def view_all(data):
    if not any(x in data['roles'] for x in ['doctor']):
        return make_response({'status': 'failure', 'message': 'unauthorised'}, 400)

    username = data['username']

    return render_template('all.html', username=username, patient_data=patient_data_dao.data)


@app.route('/patient')
@authorise
def patient(data):
    if not any(x in data['roles'] for x in ['patient']):
        return make_response({'status': 'failure', 'message': 'unauthorised'}, 400)

    username = data['username']

    patient_data = chain.from_iterable(
        map(lambda x: x['records'],
            filter(lambda x: x['username'] == username,
                   patient_data_dao.data
                   )
            )
    )

    return render_template('patient.html', username=username, patient_data=patient_data)


@app.route('/logout')
@authorise
def logout(data):
    del session['authentication']
    return redirect('/')


@app.route('/')
@authorise
def index(data):
    return render_template('index.html', roles=data['roles'])


if __name__ == '__main__':
    try:
        app.run(port=2222, debug=True)
    finally:
        patient_data_dao.save()

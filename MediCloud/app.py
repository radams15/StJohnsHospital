import os
import re
import sys
import uuid

sys.path.append('../shared')

import Authorisation

from flask import *
from dotenv import load_dotenv

from FileDao import FileDao

load_dotenv('../.env')

app = Flask(__name__)
app.secret_key = uuid.uuid4().hex

secret = os.getenv('SECRET')
auth_addr = os.getenv('AUTH_ADDR')

file_dao = FileDao('data.json', secret)

authorise = Authorisation.create_authorisation(secret, auth_addr, "http://localhost:5555")


@app.route('/callback')
def callback():
    tok = request.args.get('token')
    if tok:
        session['authentication'] = tok
        return redirect('/')
    else:
        return make_response({'status': 'failure', 'message': 'invalid authorisation token'})


@app.route('/files')
@authorise
def files(data):
    files = filter(lambda x: x['owner'] == data['username'] or data['username'] in x['shared'],
                   file_dao.data)

    return render_template('files.html', files=files)

@app.route('/upload', methods=['POST'])
@authorise
def upload_file(data):
    file = request.files['file']
    shared = filter(lambda x: x, map(str.strip, re.split(r'[\s,;]', request.form['shared']) or []))
    if not file or file.filename == '':
        flash('No selected file')
        return redirect(request.url)

    filename = os.path.basename(file.filename)
    file_dao.add_file(data['username'], filename, shared, file.stream.read())

    return redirect('/files')

@app.route('/upload', methods=['GET'])
@authorise
def upload_file_page(data):
    return render_template('upload.html')


@app.route('/file/<filename>/view', methods=['GET'])
@authorise
def file(data, filename):
    try:
        file = file_dao.get_file(os.path.basename(filename))
        return make_response(file, 200)
    except FileNotFoundError as e:
        print(e)
        return make_response({
            'status': 'failure',
            'message': 'invalid path'
        }, 404)

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
    app.run(port=5555, debug=True, threaded=True, processes=1)

import subprocess
import atexit
import os

from sys import argv
from os.path import abspath

CERT = abspath('./localhost.pem')
KEY = abspath('./localhost.key')

PROJECTS = {
        'sso': 1111,
        'FinCare': 3333,
        'CareConnect': 3355,
        'MediCloud': 5555,
        'MedRecords': 2222,
        'Prescriptions': 4444
}

env = os.environ.copy()


def run_single(name, host, secret):
    port = PROJECTS[name]
    env['SECRET'] = secret
    return subprocess.Popen(['flask', 'run', f'--host={host}', f'--port={port}', f'--cert={CERT}', f'--key={KEY}'], cwd=name, env=env)


processes = []

secret = input('Secret key: ')

for project in PROJECTS.keys():
    processes.append(run_single(project, 'localhost', secret))


def on_exit():
    print('Terminating Processes')
    for p in processes:
        p.terminate()


atexit.register(on_exit)

input('Press return to exit...')

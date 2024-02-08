import json


class PatientDataDao(object):
    def __init__(self, file):
        self.file = file
        with open(self.file, 'r') as f:
            self.data = json.load(f)

    def save(self):
        with open(self.file, 'w') as f:
            json.dump(self.data, f, indent=1)
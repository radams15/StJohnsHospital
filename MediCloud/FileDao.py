import json
import os.path


class FileDao(object):
    def __init__(self, file):
        self.file = file
        self.storage_path = './store'
        with open(self.file, 'r') as f:
            self.data = json.load(f)

    def add_file(self, username, file_name, shared, file_content):
        self.data.append({
            'owner': username,
            'shared': shared,
            'name': file_name
        })

        with open(os.path.join(self.storage_path, file_name), 'wb') as f:
            f.write(file_content)

        self.save()

    def get_file(self, file_name):
        with open(os.path.join(self.storage_path, file_name), 'r') as f:
            return f.read()
    def save(self):
        with open(self.file, 'w') as f:
            json.dump(self.data, f, indent=1)
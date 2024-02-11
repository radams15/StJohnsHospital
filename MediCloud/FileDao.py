import os
import json
from base64 import b64encode, b64decode
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

from EncryptedJsonFile import EncryptedJsonFile


class FileDao(EncryptedJsonFile):
    def __init__(self, file, key):
        super().__init__(file, key, encrypted=True)

        self.storage_path = './store'

    def add_file(self, username, file_name, shared, file_content):
        key = get_random_bytes(16)
        cipher = AES.new(key, AES.MODE_CBC)
        ct_bytes = cipher.encrypt(pad(file_content, AES.block_size))
        iv = b64encode(cipher.iv).decode('utf-8')

        self.data.append({
            'owner': username,
            'shared': list(shared),
            'name': file_name,
            'iv': iv,
            'key': b64encode(key).decode('utf-8')
        })

        with open(os.path.join(self.storage_path, file_name), 'wb') as f:
            f.write(ct_bytes)

        self.save()

    def get_file(self, file_name):
        metadata = next(filter(lambda x: x['name'] == file_name, self.data))

        with open(os.path.join(self.storage_path, file_name), 'rb') as f:
            data = f.read()

        iv = b64decode(metadata['iv'])
        cipher = AES.new(b64decode(metadata['key']), AES.MODE_CBC, iv)
        pt = unpad(cipher.decrypt(data), AES.block_size)

        return pt

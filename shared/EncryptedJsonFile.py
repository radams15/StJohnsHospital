import json
from hashlib import sha256
from base64 import b64encode, b64decode

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad


class EncryptedJsonFile(object):
    def __init__(self, file, key, encrypted=True):
        self.file = file
        self.encrypted = encrypted
        self.key = sha256(key.encode()).hexdigest()[:16].encode()

        with open(self.file, 'r') as f:
            data = json.load(f)

        if 'ciphertext' in data:  # stored encrypted
            iv = b64decode(data['iv'])
            ct = b64decode(data['ciphertext'])
            cipher = AES.new(self.key, AES.MODE_CBC, iv)
            pt = unpad(cipher.decrypt(ct), AES.block_size)

            self.data = json.loads(pt)
        else:
            self.data = data

    def save(self):    
        if self.encrypted:
            data = json.dumps(self.data).encode()

            cipher = AES.new(self.key, AES.MODE_CBC)
            ct_bytes = cipher.encrypt(pad(data, AES.block_size))
            iv = b64encode(cipher.iv).decode('utf-8')
            ct = b64encode(ct_bytes).decode('utf-8')
            to_dump = {'iv': iv, 'ciphertext': ct}
        else:
            to_dump = self.data

        with open(self.file, 'w') as f:
            json.dump(to_dump, f, indent=1)

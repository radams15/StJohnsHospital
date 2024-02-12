import json
import sys

sys.path.append('../shared')

from EncryptedJsonFile import EncryptedJsonFile

class UserDao(EncryptedJsonFile):
    def __init__(self, file, key):
        super().__init__(file, key, encrypted=True)

    def get_user(self, username):
        try:
            return next(filter(lambda x: x['username'] == username, self.data["users"]))
        except StopIteration:  # No users with that name
            return None

    def user_roles(self, username):
        return map(lambda x: (x, self.data['roles'][x]), self.get_user(username)["roles"])

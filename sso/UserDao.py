import json


class UserDao(object):
    def __init__(self, file):
        self.file = file
        with open(self.file, 'r') as f:
            self.data = json.load(f)

    def get_user(self, username):
        try:
            return next(filter(lambda x: x['username'] == username, self.data["users"]))
        except StopIteration:  # No users with that name
            return None

    def user_roles(self, username):
        return map(lambda x: (x, self.data['roles'][x]), self.get_user(username)["roles"])

    def close(self):
        with open(self.file, 'w') as f:
            json.dump(self.data, f, indent=1)

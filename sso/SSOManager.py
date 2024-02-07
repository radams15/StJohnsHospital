from hashlib import sha256

from UserDao import UserDao


class SSOManager(object):
    def __init__(self, user_dao: UserDao):
        self.user_dao = user_dao

    def validate_user(self, username, password) -> bool:
        info = self.user_dao.get_user(username)

        if info is None:
            return False

        _, pass_hash = info

        salt, hash = pass_hash.split(':')

        return sha256((salt + password).encode()).hexdigest() == hash
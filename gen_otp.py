from sys import argv, path

import pyotp

path.append('./shared')
from sso.UserDao import UserDao


if len(argv) != 3:
    print(f'Usage: {argv[0]} SECRET USERNAME')
    exit(1)

user_dao = UserDao('sso/users.json', argv[1])

user = user_dao.get_user(argv[2])

totp = pyotp.TOTP(user['secret'])
otp = totp.now()
print(f'{user["username"]}: {otp}')

from sys import argv

import pyotp

from UserDao import UserDao

if len(argv) != 3:
    print(f'Usage: {argv[0]} SECRET USERNAME')
    exit(1)

user_dao = UserDao('users.json', argv[1])

user = user_dao.get_user(argv[2])

totp = pyotp.TOTP(user['secret'])
otp = totp.now()
print(f'{user["username"]}: {otp}')

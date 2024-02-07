import sqlite3
from hashlib import sha256
import uuid
from threading import Lock


class UserDao(object):
    def __init__(self, file):
        self._db = sqlite3.connect(file, check_same_thread=False)
        self._lock = Lock()
        self._init_db()
        self._populate()

    def _init_db(self):
        with self._lock:
            c = self._db.cursor()
            c.execute('''
            CREATE TABLE IF NOT EXISTS User (
                Username     TEXT  UNIQUE PRIMARY KEY NOT NULL,
                PasswordHash TEXT NOT NULL
            );
            ''')

            c.execute('''
            CREATE TABLE IF NOT EXISTS Role (
                Id   INTEGER  UNIQUE PRIMARY KEY NOT NULL,
                Name TEXT UNIQUE
            );
            ''')

            c.execute('''
            CREATE TABLE IF NOT EXISTS RoleMembership (
                Username TEXT REFERENCES User(Username),
                RoleId  INTEGER REFERENCES Role(Id)
            );
            ''')
            c.close()

    def get_user(self, username):
        with self._lock:
            c = self._db.cursor()
            c.execute('SELECT * FROM User WHERE Username = ?', (username,))
            return c.fetchone()

    def get_role(self, name):
        with self._lock:
            c = self._db.cursor()
            c.execute('SELECT * FROM Role WHERE Name = ?', (name,))
            return c.fetchone()

    def user_roles(self, name):
        with self._lock:
            c = self._db.cursor()
            c.execute('SELECT Id, Name FROM RoleMembership JOIN Role ON RoleMembership.RoleId = Role.Id WHERE RoleMembership.Username = ?', (name,))
            return c.fetchall()

    def _populate(self):
        users = [
            ('patient1', 'pass', ['patient']),
            ('patient2', 'pass', ['patient']),
            ('pharmacist1', 'pass', ['pharmacist']),
            ('doctor1', 'pass', ['doctor']),
            ('finance1', 'pass', ['finance']),
            ('partner1', 'pass', ['partner']),
            ('partner2', 'pass', ['partner']),
        ]

        roles = [
            'patient',
            'doctor',
            'finance',
            'pharmacist',
            'partner'
        ]

        role_ids = [

        ]

        for role_name in roles:
            if self.get_role(role_name) is None:
                with self._lock:
                    c = self._db.cursor()
                    c.execute('INSERT INTO Role VALUES (null, ?)', (role_name, ))
                    c.execute('SELECT last_insert_rowid()')
                    role_ids.append(c.fetchone()[0]) # add id of role
                    c.close()

        for username, password, user_roles in users:
            if self.get_user(username) is None:
                salt = uuid.uuid4().hex
                hashed_pw = ':'.join([salt, sha256((salt + password).encode()).hexdigest()])
                with self._lock:
                    c = self._db.cursor()
                    c.execute('INSERT INTO User VALUES (?, ?)', (username, hashed_pw))
                    c.close()

                for role in user_roles:
                    id = role_ids[roles.index(role)]
                    with self._lock:
                        c = self._db.cursor()
                        c.execute('INSERT INTO RoleMembership VALUES (?, ?)', (username, id))
                        c.close()

    def __del__(self):
        with self._lock:
            self._db.commit()
            self._db.close()
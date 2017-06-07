from flask.ext.login import UserMixin
from db import mysql

class UserNotFoundError(Exception):
    pass


class User(UserMixin):

    id = None
    password = None

    def __init__(self, id):
        cur = mysql.connect().cursor()
        cur.execute('''SELECT user_name, user_fb_id FROM cnl.user''')
        rv = cur.fetchall()
        USERS = dict(rv)
        if id not in USERS:
            raise UserNotFoundError()
        self.id = id
        self.password = USERS[id]

    @classmethod
    def get(cls, id):
        try:
            return cls(id)
        except UserNotFoundError:
            return None

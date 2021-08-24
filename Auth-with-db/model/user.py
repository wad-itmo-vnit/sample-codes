import random
import string
from werkzeug.security import generate_password_hash, check_password_hash
import app_config
import os

def gen_session_token(length=24):
    token = ''.join([random.choice(string.ascii_letters + string.digits) for i in range(length)])
    return token

class User:
    def __init__(self, db, username, password, token=None):
        self.db = db
        self.username = username
        self.password = password
        self.token = token

        # Using file-database
        # self.dump_to_file()
    
    @classmethod
    def new(cls, db, username, password):
        password = generate_password_hash(password)

        # Save to database
        db.users.insert({ "username": username, "password": password })

        return cls(db, username, password)
    
    @classmethod
    def from_file(cls, filename):
        with open(app_config.USER_DB_DIR + '/' + filename, 'r') as f:
            text = f.readline().strip()
            username, password, token = text.split(';')
            if token == 'None':
                return cls(username, password)
            return cls(username, password, token)
    
    @staticmethod
    def find_user(db, username):
        # usernames = set(name[:-5] for name in os.listdir(app_config.USER_DB_DIR))
        # return username in usernames
        
        return len(list(db.users.find({"username": username}))) > 0

    @classmethod
    def get_user(cls, db, username):
        # return cls.from_file(username + ".data")

        data = db.users.find_one({"username": username})
        if "token" not in data.keys() or data["token"] == None:
            return cls(db, data["username"], data["password"])
        else:
            return cls(db, data["username"], data["password"], data["token"])
    
    def authenticate(self, password):
        return check_password_hash(self.password, password)

    def update_password(self, password):
        self.password = generate_password_hash(password)

        # Using file-database
        # self.dump_to_file()

        # update to database
        self.db.users.update_one({"username": self.username}, {"$set": {"password": self.password}})
    
    def init_session(self):
        self.token = gen_session_token()
        
        # Using file-database
        # self.dump_to_file()

        # update to database
        self.db.users.update_one({"username": self.username}, {"$set": {"token": self.token}})

        return self.token
    
    def authorize(self, token):
        return token == self.token
    
    def terminate_session(self):
        self.token = None

        # Using file-database
        # self.dump_to_file()

        # update to database
        self.db.users.update_one({"username": self.username}, {"$set": {"token": None}})
    
    def __str__(self):
        return f'{self.username};{self.password};{self.token}'
    
    def dump_to_file(self):
        with open(app_config.USER_DB_DIR + '/' + self.username + '.data', 'w') as f:
            f.write(str(self))
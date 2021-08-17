from werkzeug.security import generate_password_hash, check_password_hash
from model.session import gen_session_token, check_session_token

class User:
    def __init__(self, username, password, session=None):
        self.username = username
        self.password = password
        self.session = session
        self.dump()
    
    @classmethod
    def from_file(cls, filename):
        with open('./data/' + filename, 'r') as f:
            metadata = f.readline().strip()
            username, password, session = metadata.split(',')
            session = None if session == 'None' else session
            return cls(username, password, session)
    
    @classmethod
    def new(cls, username, password):
        password = generate_password_hash(password)
        return cls(username, password)
    
    def authenticate(self, password):
        return check_password_hash(self.password, password)
    
    def update_password(self, password):
        self.password = generate_password_hash(password)

    def init_session(self, password):
        if self.authenticate(password):
            token_key, token = gen_session_token(self.username)
            self.session = token_key
            self.dump()
            return token
        return None
    
    def authorize(self, token):
        if self.session != None:
            return check_session_token(token, self)
        return False
    
    def terminate_session(self):
        self.session = None
        self.dump()
    
    def dump(self):
        pass
        # file_name = './data/' + self.username + ".data"
        # with open(file_name, 'w') as f:
        #     f.write(str(self))
    
    def __str__(self):
        return f"{self.username},{self.password},{self.session}"
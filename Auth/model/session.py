import random
import string
import hmac
import hashlib
import app_config

def gen_session_token(username, length=app_config.SESSION_TOKEN_LENGTH):
    token_key = ''.join([random.choice(string.ascii_letters + string.digits) for i in range(length)])
    token = hmac.new(token_key.encode(), username.encode(), hashlib.sha256).hexdigest()
    return token_key, token

def check_session_token(token, user):
    return hmac.compare_digest(
        hmac.new(user.session.encode(), user.username.encode(), hashlib.sha256).hexdigest(),
        token
    )
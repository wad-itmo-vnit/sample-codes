from flask import Flask, render_template, request, redirect, make_response
from functools import wraps

app = Flask(__name__)

auth_token = "asdfklashvfgkjashdf"

# Function to generate unique token based on user or/and pwd
def generate_token(user, pwd):
    return "asdfklashvfgkjashdf"
    # return user + ':' + pwd

# Home route - always redirect to login
@app.route('/')
def home():
    return redirect('/index')

# Function to check if user is authenticated
def auth(request):
    global auth_token
    token = request.cookies.get('login-info')
    return (token == auth_token)
    # try:
    #     user, pwd = token.split(':')
    # except:
    #     return False
    # if (user == 'admin' and pwd == 'admin'):
    #     return True
    # else:
    #     return False

# Route for basic login function
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        user = request.form.get('username')
        pwd = request.form.get('password')
        if (user == 'admin' and pwd == 'admin'):
            token = generate_token(user, pwd)
            resp = make_response(redirect('/index'))
            resp.set_cookie('login-info', token)
            return resp
        else:
            return redirect('/login'), 403

# Auth required route
@app.route('/index')
def index():
    if auth(request):
        return render_template('index.html', text="Using function")
    else:
        return redirect('/')
    
# Auth checking decorator
def auth_required(f):
    @wraps(f)
    def check(*arg, **kwargs):
        if (auth(request)):
            return f(*arg, **kwargs)
        else:
            return redirect('/')
    return check

# Auth required route 2 - using decorator for auth checking
@app.route('/index2')
@auth_required
def index2():
    return render_template('index.html', text="Using decorator")

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
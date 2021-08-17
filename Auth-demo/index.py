from flask import Flask, request, render_template, make_response, redirect, flash
import app_config
from model.user import User
from functools import wraps
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = app_config.SECRET_KEY

# users = {}
# users['admin'] = User('admin', 'admin')

users = {name[:-5]:User.from_file(name) for name in os.listdir(app_config.USER_DB_DIR)}

def login_required(func):
    @wraps(func)
    def login_func(*arg, **kwargs):
        try:
            if (users[request.cookies.get('username')].authorize(request.cookies.get('token'))):
                return func(*arg, **kwargs)
        except:
            pass
        flash("Login required!!!")
        return redirect('/login')
    
    return login_func

def no_login(func):
    @wraps(func)
    def no_login_func(*arg, **kwargs):
        try:
            if (users[request.cookies.get('username')].authorize(request.cookies.get('token'))):
                flash("You're already in!")
                return redirect('/')
        except:
            pass
        return func(*arg, **kwargs)
    
    return no_login_func

@app.route('/')
def home():
    return redirect('/index')

@app.route('/index')
@login_required
def index():
    return render_template('index.html', text="Welcome to WAD VNIT 2021!!!")

@app.route('/login', methods=['POST', 'GET'])
@no_login
def login():
    if request.method == 'GET':
        return render_template('login.html')
    
    username, password = request.form.get('username'), request.form.get('password')
    if username in users.keys():
        # current_user = users[username]
        if users[username].authenticate(password):
            token = users[username].init_session()
            resp = make_response(redirect('/index'))
            resp.set_cookie('username', username)
            resp.set_cookie('token', token)
            return resp
        else:
            flash("Username or password is not correct!!!")
    else:
        flash("User does not exist")
    
    return render_template('login.html')

@app.route('/logout', methods=['POST'])
@login_required
def logout():
    username = request.cookies.get('username')
    users[username].terminate_session()
    resp = make_response(redirect('/login'))
    resp.delete_cookie('username')
    resp.delete_cookie('token')
    flash("You've logged out!!!")
    return resp

@app.route('/register', methods=['POST', 'GET'])
@no_login
def register():
    if request.method == "GET":
        return render_template('register.html')
    
    username, password, password_confirm = request.form.get('username'), request.form.get('password'), request.form.get('password_confirm')
    if username not in users.keys():
        if password == password_confirm:
            users[username] = User.new(username, password)
            token = users[username].init_session()
            resp = make_response(redirect('/index'))
            resp.set_cookie('username', username)
            resp.set_cookie('token', token)
            return resp
        else:
            flash("Passwords don't match!!!")
    else:
        flash("User already exists!!!")
    
    return render_template('register.html')

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
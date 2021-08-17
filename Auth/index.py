from flask import Flask, request, flash, redirect, render_template, make_response
from functools import wraps
import os

import app_config
from model.user import User

app = Flask(__name__)
app.config['SECRET_KEY'] = app_config.SECRET_KEY

# files = [str(file) for file in os.listdir('data')]

# users = { file[:-5]: User.from_file(file) for file in files}

users = {}
users['admin'] = User.new('admin', 'admin')

def login_required(func):
    @wraps(func)
    def login_func(*arg, **kwargs):
        if request.cookies.get('username') in users.keys():
            if users[request.cookies.get('username')].authorize(request.cookies.get('token')):
                return func(*arg, **kwargs)
        
        flash("Login required!!!")
        return redirect('/login')

    return login_func

def no_login(func):
    @wraps(func)
    def no_login_func(*arg, **kwargs):
        if request.cookies.get('username') in users.keys():
            if users[request.cookies.get('username')].authorize(request.cookies.get('token')):
                return redirect('/index')
        
        return func(*arg, **kwargs)

    return no_login_func


@app.route('/')
def home():
    return redirect('/index')

@app.route('/index')
@login_required
def index():
    return render_template('index.html', text="You're in")

@app.route('/register', methods=['GET', 'POST'])
@no_login
def register():
    if request.method == 'GET':
        return render_template('register.html')
    username, password, password_confirm = request.form.get('username'), request.form.get('password'), request.form.get('password_confirm')
    if username not in users.keys():
        if password == password_confirm:
            users[username] = User.new(username, password)
            token = users[username].init_session(password)
            if token != None:
                resp = make_response(redirect('/index'))
                resp.set_cookie('username', username)
                resp.set_cookie('token', token)
                return resp
            else:
                flash("Error init session!!!")
        else:
            flash("Passwords don't match!!!")
    else:
        flash("User already exist!!!")
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
@no_login
def login():
    if request.method == 'GET':
        return render_template('login.html')
    
    username, password = request.form.get('username'), request.form.get('password')
    if username in users.keys():
        token = users[username].init_session(password)
        if token != None:
            resp = make_response(redirect('/index'))
            resp.set_cookie('username', username)
            resp.set_cookie('token', token)
            return resp
    
    flash("Username or password is not correct!!!")
    return render_template('login.html')

@app.route('/logout', methods=['POST'])
@login_required
def logout():
    username = request.cookies.get('username')
    users[username].terminate_session()
    resp = make_response(redirect('/login'))
    resp.delete_cookie('username')
    resp.delete_cookie('token')
    return resp

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
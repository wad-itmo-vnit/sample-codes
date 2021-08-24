from flask import Flask, request, render_template, make_response, redirect, flash
import app_config
from model.user import User
from functools import wraps
import os
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config['SECRET_KEY'] = app_config.SECRET_KEY
app.config["MONGO_URI"] = "mongodb://localhost:27017/wad-vnit"
mongo = PyMongo(app)
db = mongo.db

def check_cookie(request):
    return User.get_user(db, request.cookies.get('username')).authorize(request.cookies.get('token'))

def login_required(func):
    @wraps(func)
    def login_func(*arg, **kwargs):
        try:
            if check_cookie(request):
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
            if check_cookie(request):
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
    if User.find_user(db, username):
        current_user = User.get_user(db, username)
        if current_user.authenticate(password):
            token = current_user.init_session()
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
    current_user = User.get_user(db, username)
    current_user.terminate_session()
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
    if not User.find_user(db, username):
        if password == password_confirm:
            new_user = User.new(db, username, password)
            token = new_user.init_session()
            resp = make_response(redirect('/index'))
            resp.set_cookie('username', username)
            resp.set_cookie('token', token)
            return resp
        else:
            flash("Passwords don't match!!!")
    else:
        flash("User already exists!!!")
    
    return render_template('register.html')

@app.route('/changepwd', methods=["POST", "GET"])
@login_required
def changepwd():
    if request.method == "GET":
        return render_template("changepwd.html")
    
    username = request.cookies.get("username")
    old_pwd = request.form.get('old_pwd')
    new_pwd = request.form.get('new_pwd')
    new_pwd_confirm = request.form.get('new_pwd_confirm')

    current_user = User.get_user(db, username)
    if current_user.authenticate(old_pwd):
        if new_pwd == new_pwd_confirm:
            current_user.update_password(new_pwd)
            flash("Password updated successfully!!!")
            return redirect("/")
        else:
            flash("New passwords not match!!!")
    else:
        flash("Old password is not correct!!!")
    return render_template("changepwd.html")


if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
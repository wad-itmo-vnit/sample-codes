from flask import Flask, request, render_template, redirect, Response, jsonify
from bot import get_ans, chatting
import threading
import time

from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ashkdfsgdasdfjhahsjfh'

socketio = SocketIO(app)
sending_to_socket = {}

new_mess = []

def auto_chat():
    global new_mess
    while True:
        new_mess.append(chatting())
        time.sleep(5)

auto_bot = threading.Thread(target=auto_chat)
auto_bot.start()

# Home directory
@app.route('/')
def home():
    return redirect('/socket')

# Answering route
@app.route('/chat', methods=['POST'])
def chat():
    mess = request.form.get('message')
    ans = get_ans(mess)
    return jsonify({'user': 'Bot', 'message': ans})

# Routes for short polling method
@app.route('/short')
def short():
    global new_mess
    new_mess.clear()    
    return render_template("index.html", method="short")

@app.route('/short/chat', methods=['POST'])
def short_chat():
    global new_mess
    try:
        ans = new_mess.pop()
        return jsonify({'user': 'Auto short polling', 'message': ans})
    except:
        return Response('', status=404)

# Routes for long polling method
@app.route('/long')
def long():
    global new_mess
    new_mess.clear()
    return render_template("index.html", method="long")

@app.route('/long/chat', methods=['POST'])
def long_chat():
    global new_mess
    while len(new_mess) < 1:
        pass
    ans = new_mess.pop()
    return jsonify({'user': 'Auto long polling', 'message': ans})

# Routes for websocket method
@app.route('/socket')
def socket():
    global new_mess
    new_mess.clear()
    return render_template("index.html", method="socket")

@socketio.on('connect')
def on_connect(data):
    sending_to_socket[request.sid] = True
    auto = threading.Thread(target=send_random_to_socket, args=(request.sid,))
    auto.start()

@socketio.on('disconnect')
def on_disconnect(data):
    sending_to_socket[request.sid] = False

@socketio.on('message')
def on_message(data, methods=['GET', 'POST']):
    ans = get_ans(data.get('message'))
    socketio.emit('message', {'user': 'Bot', 'message': ans}, room=request.sid)

def send_random_to_socket(sid):
    while sending_to_socket[sid]:
        try:
            ans = new_mess.pop()
            socketio.send({'user': 'Auto socket', 'message': ans}, to=sid)
        except:
            pass

if __name__ == "__main__":
    socketio.run(app, debug=True)
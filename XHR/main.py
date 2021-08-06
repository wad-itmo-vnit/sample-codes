from flask import Flask, render_template, request, Response
import time
import threading

app = Flask(__name__)
app.debug = True

cnt = 0
old = 0

def incr():
    global cnt;
    while True:
        time.sleep(1)
        cnt += 1

thread = threading.Thread(target=incr)
thread.start()

# XMLHttpRequest
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/add', methods=['POST'])
def addition():
    a = request.form.get('a')
    b = request.form.get('b')

    result = int(a) + int(b)

    return str(result)

# Short polling
@app.route('/short', methods=['GET', 'POST'])
def short_handler():
    global cnt
    if request.method == 'GET':
        return render_template('short.html')
    elif request.method == 'POST':
        if cnt % 10 == 0:
            return str(cnt)
        else:
            return 'error'
    else:
        return Response('', status=405)

# Long polling
@app.route('/long', methods=['GET', 'POST'])
def long_handler():
    global cnt
    global old
    if request.method == 'GET':
        return render_template('long.html')
    elif request.method == 'POST':
        while (cnt % 5 != 0) or (cnt == old):
            pass
        old = cnt
        return str(cnt)
    else:
        return Response('', status=405)


if __name__ == '__main__':
    app.run()
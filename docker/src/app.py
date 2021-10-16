from flask import Flask, json, jsonify

app = Flask(__name__)

@app.route('/')
def hello():
    return jsonify(greeting='hello world')

if __name__ == '__main__':
    app.run(port=5000, host='0.0.0.0')
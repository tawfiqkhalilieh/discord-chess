from flask import Flask, send_file
from threading import Thread

app = Flask('')


@app.route('/')
def main():
    return "server online!"


@app.route('/chess')
def chess():
    return send_file("chess5.svg", mimetype='image/svg+xml')


def run():
    app.run(host="0.0.0.0", port=8080)


def keep_alive():
    server = Thread(target=run)
    server.start()

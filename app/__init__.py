from flask import Flask

app = Flask(__name__)

def init_app():
    return app
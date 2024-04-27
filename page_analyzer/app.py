#!/usr/bin/env python3
import flask

app = flask.Flask(__name__)


@app.route('/')
def main():
    return 'Hello world!'

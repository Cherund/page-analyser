#!/usr/bin/env python3
import flask

app = flask.Flask(__name__)


@app.route('/')
def main():
    return flask.render_template('index.html')


@app.route('/urls')
def get_urls():
    return flask.render_template('urls.html')

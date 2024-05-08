#!/usr/bin/env python3
import flask
from page_analyzer.utils import add_item, get_item


app = flask.Flask(__name__)


@app.route('/')
def main():
    return flask.render_template('index.html')


@app.route('/urls')
def get_urls():
    return flask.render_template('urls.html')


@app.route('/url/<int:url_id>')
def show_url_page(url_id):
    url = get_item(url_id)
    return flask.render_template('url.html', url=url.name,
                                 id=url.id, date=url.created_at)


@app.post('/url')
def add_url():
    url = flask.request.form.get('url')
    url_id = add_item(url)
    return flask.redirect(flask.url_for('show_url_page', url_id=url_id))

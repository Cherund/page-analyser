#!/usr/bin/env python3
import flask
from page_analyzer.utils import (add_item, get_item,
                                 check_url, normalize_url,
                                 get_all, get_env_var)


app = flask.Flask(__name__)
app.secret_key = get_env_var('SECRET_KEY')


@app.route('/')
def main():
    messages = flask.get_flashed_messages(with_categories=True)
    return flask.render_template('index.html', messages=messages,)


@app.route('/urls')
def get_urls():
    urls = get_all()
    return flask.render_template('urls.html', urls=urls)


@app.route('/url/<int:url_id>')
def show_url_page(url_id):
    url = get_item(url_id)
    return flask.render_template('url.html', url=url.name,
                                 id=url.id, date=url.created_at)


@app.post('/url')
def add_url():
    url = flask.request.form.get('url')
    message = check_url(url)
    if message:
        flask.flash(message, 'error')
        return flask.redirect(flask.url_for('main'))

    url = normalize_url(url)
    url_id = add_item(url)
    return flask.redirect(flask.url_for('show_url_page', url_id=url_id))

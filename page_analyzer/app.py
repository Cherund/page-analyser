#!/usr/bin/env python3
import flask
from page_analyzer.utils import (add_item, get_item, check_url,
                                 normalize_url, get_all, get_env_var,
                                 add_check, get_checks)


app = flask.Flask(__name__)
app.secret_key = get_env_var('SECRET_KEY')


@app.route('/')
def main():
    messages = flask.get_flashed_messages(with_categories=True)
    return flask.render_template('index.html', messages=messages,)


@app.route('/urls')
def get_urls():
    urls = get_all('urls')
    checks = get_all('url_checks')
    return flask.render_template('urls.html', urls=urls, checks=checks)


@app.route('/urls/<url_id>')
def show_url_page(url_id):
    url = get_item(url_id)
    checks = get_checks(url_id)
    messages = flask.get_flashed_messages(with_categories=True)
    return flask.render_template('url.html', url=url, checks=checks,
                                 messages=messages)


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


@app.post('/urls/<int:url_id>/checks')
def check_url_page(url_id):
    message = add_check(url_id)
    if message:
        flask.flash(message, 'error')

    return flask.redirect(flask.url_for('show_url_page', url_id=url_id))

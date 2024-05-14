#!/usr/bin/env python3
import flask
from page_analyzer.db_manager import (add_item, get_item, get_urls_last_check,
                                      add_check, get_url_checks)
from page_analyzer.utils import check_url, normalize_url, get_env_var


app = flask.Flask(__name__)
app.secret_key = get_env_var('SECRET_KEY')


@app.route('/')
def main():
    messages = flask.get_flashed_messages(with_categories=True)
    return flask.render_template('index.html', messages=messages,)


@app.route('/urls')
def get_urls():
    urls_check = get_urls_last_check()
    return flask.render_template('urls.html', urls_check=urls_check)


@app.route('/urls/<url_id>')
def show_url_page(url_id):
    url = get_item(url_id)
    checks = get_url_checks(url_id)
    messages = flask.get_flashed_messages(with_categories=True)
    return flask.render_template('url.html', url=url, checks=checks,
                                 messages=messages)


@app.post('/url')
def add_url():
    url = flask.request.form.get('url')
    message = check_url(url)
    flask.flash(*message)
    if 'danger' in message:
        return flask.redirect(flask.url_for('main'))

    url = normalize_url(url)
    url_id = add_item(url)
    return flask.redirect(flask.url_for('show_url_page', url_id=url_id))


@app.post('/urls/<int:url_id>/checks')
def check_url_page(url_id):
    message = add_check(url_id)
    if message:
        flask.flash(*message)

    return flask.redirect(flask.url_for('show_url_page', url_id=url_id))

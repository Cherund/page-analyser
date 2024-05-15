#!/usr/bin/env python3
import flask
from page_analyzer.db_manager import (add_item, get_item,
                                      get_urls_last_check, add_check,
                                      get_url_checks, check_url_exists)
from page_analyzer.utils import check_url, normalize_url, get_env_var


app = flask.Flask(__name__)
app.secret_key = get_env_var('SECRET_KEY')


@app.route('/')
def main():
    return flask.render_template('index.html',)


@app.route('/urls')
def get_urls():
    messages = flask.get_flashed_messages(with_categories=True)
    if messages:
        return flask.render_template('index.html', messages=messages, ), 422
    urls_check = get_urls_last_check()
    return flask.render_template('urls.html', urls_check=urls_check)


@app.route('/urls/<int:url_id>')
def show_url_page(url_id):
    url = get_item(url_id)
    checks = get_url_checks(url_id)
    messages = flask.get_flashed_messages(with_categories=True)

    return flask.render_template('url.html', url=url, checks=checks,
                                 messages=messages)


@app.post('/url')
def add_url():
    url = flask.request.form.get('url')
    url = normalize_url(url)
    url_info = check_url_exists(url)
    message = check_url(url, url_info)
    flask.flash(*message)
    if 'danger' in message:
        return flask.redirect(flask.url_for('get_urls'))

    if url_info:
        url_id = url_info.id
    else:
        url_id = add_item(url)
    return flask.redirect(flask.url_for('show_url_page', url_id=url_id))


@app.post('/urls/<int:url_id>/checks')
def check_url_page(url_id):
    message = add_check(url_id)
    flask.flash(*message)

    return flask.redirect(flask.url_for('show_url_page', url_id=url_id))

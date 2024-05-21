from flask import (Flask, render_template, redirect,
                   flash, url_for, request, abort)
from page_analyzer import db_manager as db
from dotenv import load_dotenv
import os
from page_analyzer.utils import validate_url, normalize_url
from page_analyzer.bs_util import get_url_info
import requests

app = Flask(__name__)
load_dotenv()
app.secret_key = os.getenv('SECRET_KEY')
app.config['DATABASE_URL'] = os.getenv('DATABASE_URL')


@app.route('/')
def main():
    return render_template('index.html')


@app.route('/urls')
def get_urls():
    connect = db.connect_db(app)
    urls_check = db.get_urls_last_check(connect)
    db.close(connect)
    return render_template('urls.html', urls_check=urls_check)


@app.route('/urls/<int:url_id>')
def show_url_page(url_id):
    connect = db.connect_db(app)
    url = db.get_url(connect, url_id)
    if not url:
        abort(404)

    checks = db.get_url_checks(connect, url_id)
    db.close(connect)
    return render_template('url.html', url=url, checks=checks)


@app.errorhandler(404)
def page_not_found(_):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def internal_error(_):
    return render_template('errors/500.html'), 500


@app.post('/urls')
def add_url():
    url = request.form.get('url')
    normal_url = normalize_url(url)
    validation_error = validate_url(normal_url)
    if validation_error:
        flash(validation_error, 'danger')
        return render_template('index.html'), 422

    connect = db.connect_db(app)
    url_info = db.check_url_exists(connect, normal_url)
    if url_info:
        flash('Страница уже существует', 'info')
        url_id = url_info.id
    else:
        flash('Страница успешно добавлена', 'success')
        url_id = db.insert_url(connect, normal_url)

    db.close(connect)
    return redirect(url_for('show_url_page', url_id=url_id))


@app.post('/urls/<int:url_id>/checks')
def check_url_page(url_id):
    connect = db.connect_db(app)
    url = db.get_url(connect, url_id).name
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException:
        flash('Произошла ошибка при проверке', 'danger')
        return redirect(url_for('show_url_page', url_id=url_id))

    url_info = get_url_info(response)
    flash('Страница успешно проверена', 'success')
    db.insert_check(connect, url_id, url_info)
    db.close(connect)

    return redirect(url_for('show_url_page', url_id=url_id))

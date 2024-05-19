from flask import (Flask, render_template, redirect,
                   flash, url_for, request, abort)
from page_analyzer import db_manager as db
from dotenv import load_dotenv
import os
from page_analyzer.utils import validate_url, normalize_url
from page_analyzer.bs_util import get_url_info


app = Flask(__name__)
load_dotenv()
app.secret_key = os.getenv('SECRET_KEY')


@app.route('/')
def main():
    return render_template('index.html')


@app.route('/urls')
def get_urls():

    urls_check = db.get_urls_last_check()
    return render_template('urls.html', urls_check=urls_check)


@app.route('/urls/<int:url_id>')
def show_url_page(url_id):
    url = db.get_item(url_id)
    if not url:
        abort(404)

    checks = db.get_url_checks(url_id)
    return render_template('url.html', url=url, checks=checks)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('errors/404.html'), 404


@app.post('/urls')
def add_url():
    url = request.form.get('url')
    normal_url = normalize_url(url)
    validation_error = validate_url(normal_url)
    if validation_error:
        flash(validation_error, 'danger')
        return render_template('index.html'), 422

    url_info = db.check_url_exists(normal_url)
    if url_info:
        flash('Страница уже существует', 'info')
        url_id = url_info.id
    else:
        flash('Страница успешно добавлена', 'success')
        url_id = db.add_item(normal_url)

    return redirect(url_for('show_url_page', url_id=url_id))


@app.post('/urls/<int:url_id>/checks')
def check_url_page(url_id):
    url = db.get_item(url_id).name
    url_info = get_url_info(url)
    if url_info:
        flash('Страница успешно проверена', 'success')
        db.add_check(url_id, url_info)
    else:
        flash('Произошла ошибка при проверке', 'danger')

    return redirect(url_for('show_url_page', url_id=url_id))

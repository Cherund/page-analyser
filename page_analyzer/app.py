#!/usr/bin/env python3
import flask
import psycopg2
from psycopg2.extras import NamedTupleCursor

app = flask.Flask(__name__)
DATABASE_URL = 'postgresql://pguser:pgpass@localhost:5432/pgdb'


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


def add_item(url):
    conn = psycopg2.connect(DATABASE_URL)
    with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
        curs.execute(
                'INSERT INTO urls (name) VALUES (%s) '
                'RETURNING id;',
                (url, )
        )
        conn.commit()
        return curs.fetchone().id


def get_item(url_id):
    conn = psycopg2.connect(DATABASE_URL)
    with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
        curs.execute(
            'SELECT * FROM urls WHERE id=(%s);', (url_id, )
        )
        return curs.fetchone()

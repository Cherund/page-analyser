import os
import validators
import psycopg2
from psycopg2.extras import NamedTupleCursor
from dotenv import load_dotenv
from urllib.parse import urlparse
import requests
# from bs4 import BeautifulSoup


def get_env_var(var_name):
    load_dotenv()
    return os.environ.get(var_name)


def check_url(url):
    if len(url) > 255:
        return 'URL exceeds 255 symbols'

    if not validators.url(url):
        return 'Incorrect URL'


def normalize_url(url):
    parsed_url = urlparse(url)
    return f'{parsed_url.scheme}://{parsed_url.netloc}'


def add_item(url):
    conn = psycopg2.connect(get_env_var('DATABASE_URL'))
    with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
        curs.execute(
                'INSERT INTO urls (name) VALUES (%s) '
                'RETURNING id;',
                (url, )
        )
        conn.commit()
        return curs.fetchone().id


def get_item(url_id):
    conn = psycopg2.connect(get_env_var('DATABASE_URL'))
    with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
        curs.execute(
            'SELECT * FROM urls WHERE id=(%s);', (url_id, )
        )
        return curs.fetchone()


def get_all(table_name):
    conn = psycopg2.connect(get_env_var('DATABASE_URL'))
    with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
        curs.execute(
            f'SELECT * FROM {table_name}',
        )
        return curs.fetchall()[::-1]


def add_check(url_id):
    url = get_item(url_id).name

    try:
        url_response = requests.get(url)
    except requests.exceptions.ConnectionError:
        return 'Error occurred during check'


    conn = psycopg2.connect(get_env_var('DATABASE_URL'))
    with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
        curs.execute(
                'INSERT INTO url_checks (url_id, status_code) VALUES (%s, %s);',
                (url_id, url_response.status_code,)
        )
        conn.commit()


def get_checks(url_id):
    conn = psycopg2.connect(get_env_var('DATABASE_URL'))
    with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
        curs.execute(
            'SELECT * FROM url_checks WHERE url_id=(%s)',
            (url_id, )
        )
        return curs.fetchall()[::-1]

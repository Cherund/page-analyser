import os
import validators
import psycopg2
from psycopg2.extras import NamedTupleCursor
from dotenv import load_dotenv
from urllib.parse import urlparse


def add_item(url):
    DATABASE_URL = get_env_var('DATABASE_URL')
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
    DATABASE_URL = get_env_var('DATABASE_URL')
    conn = psycopg2.connect(DATABASE_URL)
    with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
        curs.execute(
            'SELECT * FROM urls WHERE id=(%s);', (url_id, )
        )
        return curs.fetchone()


def check_url(url):
    if len(url) > 255:
        return 'URL exceeds 255 symbols'

    if not validators.url(url):
        return 'Incorrect URL'


def normalize_url(url):
    parsed_url = urlparse(url)
    return f'{parsed_url.scheme}://{parsed_url.netloc}'


def get_env_var(var_name):
    load_dotenv()
    return os.environ.get(var_name)


def get_all():
    DATABASE_URL = get_env_var('DATABASE_URL')
    conn = psycopg2.connect(DATABASE_URL)
    with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
        curs.execute(
            'SELECT * FROM urls',
        )
        return list(curs.fetchall()[::-1])

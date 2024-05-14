import requests
import psycopg2
from psycopg2.extras import NamedTupleCursor
from page_analyzer.utils import get_env_var, get_tag_str


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


def get_websites():
    conn = psycopg2.connect(get_env_var('DATABASE_URL'))
    with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
        curs.execute(
            'SELECT name FROM urls',
        )
        return curs.fetchall()


def add_check(url_id):
    url = get_item(url_id).name

    try:
        url_response = requests.get(url)
    except requests.exceptions.ConnectionError:
        return 'Произошла ошибка при проверке', 'danger'
        # return 'Error occurred during check', 'danger'

    h1 = get_tag_str(url_response.content, 'h1')
    title = get_tag_str(url_response.content, 'title')
    description = get_tag_str(url_response.content, 'meta',
                              {'name': "description"})

    conn = psycopg2.connect(get_env_var('DATABASE_URL'))
    with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
        curs.execute(
                'INSERT INTO url_checks (url_id, status_code, '
                'h1, title, description) '
                'VALUES (%s, %s, %s, %s, %s);',
                (url_id, url_response.status_code, h1, title, description)
        )
        conn.commit()
    return 'Страница успешно проверена', 'success'


def get_url_checks(url_id):
    conn = psycopg2.connect(get_env_var('DATABASE_URL'))
    with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
        curs.execute(
            'SELECT * FROM url_checks WHERE url_id=(%s) ORDER BY id DESC',
            (url_id, )
        )
        return curs.fetchall()


def get_urls_last_check():
    conn = psycopg2.connect(get_env_var('DATABASE_URL'))
    with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
        curs.execute('SELECT DISTINCT ON (urls.id) '
                     'urls.id AS id, '
                     'url_checks.id AS check_id, '
                     'url_checks.status_code AS status_code, '
                     'url_checks.created_at AS created_at, '
                     'urls.name AS name '
                     'FROM urls '
                     'LEFT JOIN url_checks ON urls.id=url_checks.url_id '
                     'ORDER BY urls.id DESC, check_id DESC;')
        return curs.fetchall()

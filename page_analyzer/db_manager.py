import psycopg2
from psycopg2.extras import NamedTupleCursor
from functools import wraps


def connect_db(app):
    return psycopg2.connect(app.config['DATABASE_URL'])


def commit(conn):
    conn.commit()


def close(conn):
    conn.close()


def with_commit(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        conn = None
        try:
            conn = args[0]
            result = func(*args, **kwargs)
            conn.commit()
            return result
        except Exception as e:
            if conn:
                conn.rollback()
            raise e
        # finally:
        #     if conn:
        #         conn.close()
    return wrapper


@with_commit
def insert_url(conn, url):
    with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
        curs.execute(
            'INSERT INTO urls (name) VALUES (%s) RETURNING id;',
            (url, )
        )
        return curs.fetchone().id


def get_url(conn, url_id):
    with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
        curs.execute(
            'SELECT * FROM urls WHERE id=(%s);', (url_id, )
        )
        return curs.fetchone()


def check_url_exists(conn, url):
    with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
        curs.execute(
            'SELECT id, name FROM urls WHERE name=(%s)',
            (url, )
        )
        return curs.fetchone()


@with_commit
def insert_check(conn, url_id, url_info):
    with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
        curs.execute(
            'INSERT INTO url_checks (url_id, status_code, '
            'h1, title, description) '
            'VALUES (%s, %s, %s, %s, %s);',
            (url_id, url_info['status_code'], url_info['h1'],
             url_info['title'], url_info['description'])
        )


def get_url_checks(conn, url_id):
    with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
        curs.execute(
            'SELECT * FROM url_checks WHERE url_id=(%s) ORDER BY id DESC',
            (url_id, )
        )
        return curs.fetchall()


def get_urls_last_check(conn):
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

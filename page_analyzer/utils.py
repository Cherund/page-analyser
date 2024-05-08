import psycopg2
from psycopg2.extras import NamedTupleCursor


DATABASE_URL = 'postgresql://pguser:pgpass@localhost:5432/pgdb'


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

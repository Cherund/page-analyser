import os
import validators
from dotenv import load_dotenv
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import requests


def get_env_var(var_name):
    load_dotenv()
    return os.environ.get(var_name)


def check_url(url, url_info):
    if len(url) > 255:
        return 'URL превышает 255 символов', 'danger'
        # return 'URL exceeds 255 symbols', 'danger'

    if not validators.url(url):
        return 'Некорректный URL', 'danger'
        # return 'Incorrect URL', 'danger'

    if url_info:
        return 'Страница уже существует', 'info'
        # return 'Page already exists', 'info'

    return 'Страница успешно добавлена', 'success'
    # return 'Page was successfully added', 'success'


def get_url_response(url):
    response = requests.get(url)

    if requests.Response.raise_for_status(response):
        raise requests.RequestException

    return response


def get_url_info(url):
    try:
        url_response = get_url_response(url)
    except requests.RequestException:
        return ('Произошла ошибка при проверке', 'danger'), None

    h1 = get_tag_str(url_response.content, 'h1')
    title = get_tag_str(url_response.content, 'title')
    description = get_tag_str(url_response.content, 'meta',
                              {'name': "description"})
    return (('Страница успешно проверена', 'success'),
            (url_response.status_code, h1, title, description))


def normalize_url(url):
    parsed_url = urlparse(url)
    return f'{parsed_url.scheme}://{parsed_url.netloc}'


def get_tag_str(url_content, tag, attrs={}):
    soup = BeautifulSoup(url_content, 'html.parser')
    tag_str = soup.find(name=tag, attrs=attrs)
    if tag_str:
        return tag_str.text or tag_str['content']
    else:
        return ''

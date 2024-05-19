import validators
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import requests


def validate_url(url):
    if len(url) > 255:
        return 'URL превышает 255 символов'

    if not validators.url(url):
        return 'Некорректный URL'


def get_url_response(url):
    response = requests.get(url)

    if requests.Response.raise_for_status(response):
        raise requests.RequestException

    return response


def get_url_info(url):
    try:
        url_response = get_url_response(url)
    except requests.RequestException:
        return None

    h1 = get_tag_str(url_response.content, 'h1')
    title = get_tag_str(url_response.content, 'title')
    description = get_tag_str(url_response.content, 'meta',
                              {'name': "description"})

    return url_response.status_code, h1, title, description


def normalize_url(url):
    parsed_url = urlparse(url)
    return f'{parsed_url.scheme}://{parsed_url.netloc}'


def get_tag_str(url_content, tag, attrs={}):
    soup = BeautifulSoup(url_content, 'html.parser')
    tag_str = soup.find(name=tag, attrs=attrs)
    if tag_str:
        text = tag_str.text or tag_str['content']
        if len(text) > 255:
            text = text[:252] + "..."
        return text
    else:
        return ''

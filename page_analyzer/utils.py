import os
import validators
from dotenv import load_dotenv
from urllib.parse import urlparse
from bs4 import BeautifulSoup


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


def get_tag_str(url_content, tag, attrs={}):
    soup = BeautifulSoup(url_content, 'html.parser')
    tag_str = soup.find(name=tag, attrs=attrs)
    print(tag_str)
    if tag_str:
        return tag_str.text or tag_str['content']
    else:
        return ''

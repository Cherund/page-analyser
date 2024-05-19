from bs4 import BeautifulSoup
import requests


def get_url_response(url):
    response = requests.get(url)

    if requests.Response.raise_for_status(response):
        raise requests.RequestException

    return response


def get_tag_str(url_content, tag, attrs={}):
    soup = BeautifulSoup(url_content, 'html.parser')
    tag_str = soup.find(name=tag, attrs=attrs)
    if tag_str:
        text = tag_str.text or tag_str['content']
        if len(text) > 255:
            # text_list = text.split()
            # text_list[-1] = '...'
            # return ' '.join(text_list)
            return text[:252] + '...'
        return text
    else:
        return ''


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

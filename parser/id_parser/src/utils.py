import re
from common.config import config
import logging

def get_fbgroup_id_from_url(url:str) -> str:
    url = url.strip()
    url = url.replace(' ', '')
    url = url.replace('\n', '')
    url = url.replace('http://', 'https://')
    url = url.replace('://www.','://' )
    if not url.endswith('/'):
        url = url + '/'
    patterns = [
        r'^https://facebook.com/\d{3,30}/$',
        r'^https://facebook.com/.{3,80}/$',
        r'^https://fb.com/page-\d{3,30}/$',
    ]
    for pattern in patterns:
        if re.match(pattern, url):
            url = url[:-1]
            url = url.replace('https://facebook.com/', '')
            url = url.replace('https://fb.com/page-', '')
            return url
    return ''


def get_new_urls() -> set[str]:
    new_urls = set()
    with open(config.NEW_URLS_FILE_PATH) as file:
        for line in file:
            url = line.strip()
            if get_fbgroup_id_from_url(url=url) != '':
                new_urls.add(url)
    logging.info('Urls in file: %s', len(new_urls))
    return new_urls



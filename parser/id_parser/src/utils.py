from id_parser.src.config import config
import logging


def get_new_urls() -> set[str]:
    new_urls = set()
    with open(config.NEW_URLS_FILE_PATH) as file:
        for line in file:
            url = line.strip()
            new_urls.add(url)
    logging.info('Urls in file: %s', len(new_urls))
    return new_urls


import logging
from fb.models import FbGroup as FbGroupModel
from dataclasses import dataclass
from requests.exceptions import RequestException
from id_parser.src.exceptions import MaxRowErrorCount, HtmlElementNotFound
from .fbgroup_page_provider import FbPageProvider
from common.config import config


@dataclass
class FbGroupIdsCollector:

    def __init__(self, page_provider: FbPageProvider):
        self.page_provider = page_provider
        self.__errors_count = 0

    def collect(self, items: list[FbGroupModel]) -> None:
        for i, group in enumerate(items):
            try:
                logging.info(group.url)
                group_dto = self.page_provider.provide(url=group.url)
                group.group_id = group_dto.group_id
                group.save()
                logging.info('%s:%s, id: %s', f'{i}/{len(items)}', group.url, group.group_id)
                self.__errors_count = 0
            except HtmlElementNotFound:
                logging.error('HtmlElementNotFound')
            except RequestException as error:
                error_msg = f'RequestException:{error}, \nurl:{group.url}'
                logging.error(error_msg)
                self.__errors_count += 1
                if self.__errors_count >= config.MAX_REQUEST_ERROR_ROW_COUNT:
                    self.__errors_count = 0
                    continue



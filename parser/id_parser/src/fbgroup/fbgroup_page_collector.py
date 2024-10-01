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
            if self.__errors_count >= config.MAX_REQUEST_ERROR_ROW_COUNT:
                break
            try:
                group_dto = self.page_provider.provide(url=group.url)
                group.group_id = group_dto.group_id
                group.likes_count = group_dto.likes_count
                group.followers_count = group_dto.followers_count
                group.save()
                log_string = f'{i:>4}/{len(items)}, {group.url:<50}\n{group_dto}'
                logging.info(log_string)
                self.__errors_count = 0
            except HtmlElementNotFound as error:
                logging.error('%s\nHtmlElementNotFound: %s', group.url, error)
                self.__errors_count += 1
            except RequestException as error:
                error_msg = f'RequestException: {error},\nUrl: {group.url}'
                logging.error(error_msg)
                self.__errors_count += 1




import logging
from fb.models import FbGroup as FbGroupModel
from dataclasses import dataclass
from requests.exceptions import RequestException
from ..exceptions import MaxRowErrorCount, HtmlElementNotFound
from .fbgroup_page_provider import FbPageProvider
from ..config import config


@dataclass
class FbGroupIdsCollector:

    def __init__(self, page_provider: FbPageProvider):
        self.page_provider = page_provider
        self.__errors_count = 0

    def collect(self, items: list[FbGroupModel]) -> None:
        for i, item in enumerate(items):
            try:
                logging.info(item.url)
                group = self.page_provider.provide(url=item.url)
                item.group_id = group.group_id
                item.save()
                logging.info('%s:%s, id: %s', f'{i}/{len(items)}', item.url, item.group_id)
                self.reset_error()
            except (RequestException, HtmlElementNotFound) as error:
                logging.error(str(error))
                self.up_error()

    def up_error(self):
        self.__errors_count += 1
        self.__check_errors()

    def reset_error(self):
        self.__errors_count = 0

    def __check_errors(self):
        if self.__errors_count == config.MAX_REQUEST_ERROR_ROW_COUNT:
            raise MaxRowErrorCount

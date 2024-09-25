import logging
from fb.models import FbGroup as FbGroupModel
from dataclasses import dataclass
from requests.exceptions import RequestException
from ..exceptions import MaxRowErrorCount, HtmlElementNotFound
from .fbgroup_page_provider import FbPageProvider


@dataclass
class FbGroupIdsCollector:
    page_provider: FbPageProvider

    def collect(self, items: list[FbGroupModel]) -> None:
        errors_count = 0
        for i, item in enumerate(items):
            try:
                logging.info(item.url)
                group = self.page_provider.provide(url=item.url)
                item.group_id = group.group_id
                item.save()
                logging.info('%s:%s, id: %s', f'{i}/{len(items)}', item.url, item.group_id)
                errors_count = 0
            except (RequestException, HtmlElementNotFound) as error:
                logging.error(str(error))
                errors_count += 1
                if errors_count == 5:
                    raise MaxRowErrorCount

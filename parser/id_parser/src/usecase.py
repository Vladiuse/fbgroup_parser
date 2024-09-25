import logging
from fb.models import FbGroup as FbGroupModel
from .exceptions import NoGroupsToParse
from .fbgroup.fbgroup_page_provider import FbPageProvider
from .fbgroup.fbgroup_page_converter import PageConverter
from .request_sender import FbRequestRequestSender
from .fbgroup.fbgroup_page_collector import FbGroupIdsCollector


class ParseFbGroupsIdsUseCase:

    def parse_groups_ids(self) -> None:
        groups_to_parse = self.__get_groups_to_parse_ids()
        logging.info('Groups to parse: %s', len(groups_to_parse))
        page_provider = FbPageProvider(
            converter=PageConverter(),
            request_sender=FbRequestRequestSender(),
        )
        collector = FbGroupIdsCollector(
            page_provider=page_provider,
        )
        collector.collect(items=groups_to_parse)

    def __get_groups_to_parse_ids(self) -> list[FbGroupModel]:
        groups_to_parse = list(FbGroupModel.objects.filter(group_id__isnull=True).order_by('?'))
        if len(groups_to_parse) == 0:
            raise NoGroupsToParse
        return groups_to_parse

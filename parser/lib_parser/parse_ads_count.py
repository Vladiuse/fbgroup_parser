import logging

from lib_parser.src.usecase import ParseGroupsAdsCountUseCase
from lib_parser.src.utils import get_groups_for_parse_ads_count
from common.config import config

logging.basicConfig(level=logging.INFO)

groups_to_parse = list(get_groups_for_parse_ads_count())
logging.info('Groups to parse: %s', len(groups_to_parse))
logging.info('Start Date: %s, AdsStatus: %s', config.START_DATE, config.ADS_STATUS)

collect_groups_ads_count_usecase = ParseGroupsAdsCountUseCase(
    groups_to_parse=groups_to_parse,
)
collect_groups_ads_count_usecase.parse()

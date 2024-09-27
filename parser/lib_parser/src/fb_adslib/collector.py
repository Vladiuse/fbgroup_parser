from fb.models import FbGroup as FbGroupModel
import logging
from .provider import AuthParamsProvider, AdsCountProvider
from .dto import FbLibGroupAdsCountRequest
from common.config import config
from dataclasses import dataclass
from time import sleep


@dataclass
class FbGroupsAdsCountCollector:
    auth_params_provider: AuthParamsProvider
    ads_count_provider: AdsCountProvider

    def collect(self, groups: list[FbGroupModel]) -> None:
        logging.info('Getting auth params...')
        auth_params = self.auth_params_provider.provide()
        for num, group in enumerate(groups):
            group_request = FbLibGroupAdsCountRequest(
                group_id=group.group_id,
                start_date=config.START_DATE,
                ads_status=config.ADS_STATUS,
            )
            logging.debug('Group request: %s', group_request)
            group_ads_count = self.ads_count_provider.provide(group_request=group_request, auth_params=auth_params)
            group.ads_count = group_ads_count
            group.save()
            string = f'{num}/{len(groups)} {group.url :<50} id:{group.group_id: <16} ads_count: {group_ads_count}'
            logging.info(string)
            sleep(config.ADSLIB_SLEEP_REQS)

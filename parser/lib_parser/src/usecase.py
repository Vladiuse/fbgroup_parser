from lib_parser.src.fb_adslib.collector import FbGroupsAdsCountCollector
from lib_parser.src.fb_adslib.provider import AuthParamsProvider, AdsCountProvider
from lib_parser.src.fb_adslib.convertor import FbAdsLibPageConverter, CardsAdsCountConverter
from common.request_sender import FbRequestRequestSender
from fb.models import FbGroup as FbGroupModel
from dataclasses import dataclass

COOKIES = {
    'wd': '1325x939',
}
HEADERS = {
    'authority': 'www.facebook.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'accept-language': 'uk-UA,uk;q=0.9,en-US;q=0.8,en;q=0.7',
    'dpr': '2',
    'sec-ch-prefers-color-scheme': 'dark',
    'sec-ch-ua': '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
    'sec-ch-ua-full-version-list': '"Not A(Brand";v="99.0.0.0", "Google Chrome";v="121.0.6167.75", "Chromium";v="121.0.6167.75"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-model': '""',
    'sec-ch-ua-platform': '"macOS"',
    'sec-ch-ua-platform-version': '"13.3.0"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:122.0) Gecko/20100101 Firefox/122.0',
    'viewport-width': '1325',
}

START_URL = 'https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=BY&media_type=all&q=some&search_type=keyword_unordered'

auth_provider = AuthParamsProvider(
    request_sender=FbRequestRequestSender(),
    page_converter=FbAdsLibPageConverter(),
    fbads_lib_start_url=START_URL,
    base_headers=HEADERS,
    base_cookies=COOKIES,
)
ads_count_provider = AdsCountProvider(
    request_sender=FbRequestRequestSender(),
    auth_params_provider=auth_provider,
    ads_count_converter=CardsAdsCountConverter(),
)
collector = FbGroupsAdsCountCollector(
    auth_params_provider=auth_provider,
    ads_count_provider=ads_count_provider,
)

@dataclass
class ParseGroupsAdsCountUseCase():
    groups_to_parse: list[FbGroupModel]

    def parse(self):
        collector.collect(groups=self.groups_to_parse)

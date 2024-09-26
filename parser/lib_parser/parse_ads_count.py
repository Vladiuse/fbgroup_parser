import json
from dataclasses import dataclass
from id_parser.src.request_sender import FbRequestRequestSender
from lib_parser.src.dto import FbLibAuthData

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






@dataclass
class AuthParamsProvider:
    request_sender: FbRequestRequestSender
    page_converter: FbAdsLibPageConverter

    def provide(self) -> FbLibAuthData:
        start_url = START_URL
        html = self.request_sender.get(url=start_url, headers=HEADERS, cookies=COOKIES)
        auth_params = self.page_converter.convert(html=html)
        print(auth_params)
        cookies = COOKIES
        headers = HEADERS
        cookies.update({
            'datr': auth_params['datr']
        })
        headers.update(
            {
                'origin': 'https://www.facebook.com',
                'referer': START_URL,
                'content-type': 'application/x-www-form-urlencoded'
            })
        data = {
            '__aaid': '0',
            '__user': '0',
            '__a': '1',
            '__req': '2',
            '__hs': auth_params['hs'],
            'dpr': '2',
            '__ccg': 'EXCELLENT',
            '__rev': auth_params['rev'],
            '__hsi': auth_params['hsi'],
            'lsd': auth_params['lsd'],
            '__spin_r': auth_params['spin_r'],
            '__spin_b': auth_params['spin_b'],
            '__spin_t': auth_params['spin_t'],
        }
        return FbLibAuthData(
            cookies=cookies,
            headers=headers,
            data=data,
            session_id=auth_params['session_id'],
        )



@dataclass
class AdsCountProvider:
    request_sender: FbRequestRequestSender
    auth_params_provider: AuthParamsProvider
    ads_count_converter: CardsAdsCountConverter

    def provide(self, group_id: str):
        auth_params = self.auth_params_provider.provide()
        param_string = f'active_status=active&ad_type=all&country=ALL&media_type=all&search_type=page&source=page-transparency-widget&start_date[min]=2024-09-26&start_date[max]&view_all_page_id={group_id}'
        cards_url = f'https://www.facebook.com/ads/library/async/search_ads/?session_id={auth_params.session_id}&count=30&{param_string}'
        res_text = self.request_sender.post(
            url=cards_url,
            headers=auth_params.headers,
            cookies=auth_params.cookies,
            data=auth_params.data,
        )
        print(res_text)
        ads_count = self.ads_count_converter.convert(json_string=res_text)
        print(ads_count)




auth_provider = AuthParamsProvider(
    request_sender=FbRequestRequestSender(),
    page_converter=FbAdsLibPageConverter()
)
provider = AdsCountProvider(
    request_sender=FbRequestRequestSender(),
    auth_params_provider=auth_provider,
    ads_count_converter=CardsAdsCountConverter()
)

provider.provide(group_id='198566486907133')


class AdsCountCollector:
    pass

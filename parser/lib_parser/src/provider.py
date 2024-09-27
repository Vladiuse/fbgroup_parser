import logging
from dataclasses import dataclass
from common.request_sender import FbRequestRequestSender
from .convertor import FbAdsLibPageConverter, CardsAdsCountConverter
from .dto import FbLibAuthData, FbLibGroupAdsCountRequest


@dataclass
class AuthParamsProvider:
    request_sender: FbRequestRequestSender
    page_converter: FbAdsLibPageConverter

    fbads_lib_start_url: str
    base_headers: dict
    base_cookies: dict

    def provide(self) -> FbLibAuthData:
        start_url = self.fbads_lib_start_url
        html = self.request_sender.get(url=start_url, headers=self.base_headers, cookies=self.base_cookies)
        auth_params = self.page_converter.convert(html=html)
        self.base_cookies.update({
            'datr': auth_params['datr']
        })
        self.base_headers.update(
            {
                'origin': 'https://www.facebook.com',
                'referer': self.fbads_lib_start_url,
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
            cookies=self.base_cookies,
            headers=self.base_headers,
            data=data,
            session_id=auth_params['session_id'],
        )


@dataclass
class AdsCountProvider:
    request_sender: FbRequestRequestSender
    auth_params_provider: AuthParamsProvider
    ads_count_converter: CardsAdsCountConverter

    def provide(self, group_request: FbLibGroupAdsCountRequest) -> int:
        start_time = group_request.start_date.strftime('%Y-%m-%d')
        auth_params = self.auth_params_provider.provide()
        param_string = f'active_status={group_request.ads_status.value}&ad_type=all&country=ALL&media_type=all&search_type=page&source=page-transparency-widget&start_date[min]={start_time}&start_date[max]&view_all_page_id={group_request.group_id}'
        cards_url = f'https://www.facebook.com/ads/library/async/search_ads/?session_id={auth_params.session_id}&count=30&{param_string}'
        logging.debug(cards_url)
        card_res_json_string = self.request_sender.post(
            url=cards_url,
            headers=auth_params.headers,
            cookies=auth_params.cookies,
            data=auth_params.data,
        )
        logging.debug('Raw card_res_json_string:\n%s', card_res_json_string)
        return self.ads_count_converter.convert(json_string=card_res_json_string)

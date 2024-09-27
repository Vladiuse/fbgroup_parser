import logging
import json
from .exceptions import EmptyPayload

class FbAdsLibPageConverter:

    def convert(self, html: str) -> dict:
        page_auth_params = dict()
        params_from_search = {
            'datr': ['"_js_datr":{"value":"', '"'],
            'session_id': ['sessionId":"', '"'],
            'lsd': ['"LSD",[],{"token":"', '"'],
            'hs': ['"haste_session":"', '"'],
            'rev': ['"client_revision":', ','],
            'hsi': ['"hsi":"', '"'],
            'spin_r': ['"__spin_r":', ','],
            'spin_b': ['"__spin_b":"', '"'],
            'spin_t': ['"__spin_t":', ','],
        }
        for param_key, search in params_from_search.items():
            try:
                start = html.index(search[0]) + len(search[0])
                end = html.index(search[1], start)
                param_value = html[start: end]
                page_auth_params.update({
                    param_key: param_value
                })
            except ValueError:
                raise ValueError(f'Param {param_key} not found')
        logging.debug('Page auth params:\n %s', page_auth_params)
        return page_auth_params


class CardsAdsCountConverter:

    def convert(self, json_string: str) -> int:
        json_string = json_string.replace('for (;;);', '')
        data = json.loads(json_string)
        if 'payload' not in data:
            raise EmptyPayload(str(data))
        return data['payload']['totalCount']
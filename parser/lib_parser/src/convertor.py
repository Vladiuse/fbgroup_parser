class FbAdsLibPageConverter:

    def convert(self, html: str) -> dict:
        result = dict()
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
                result.update({
                    param_key: param_value
                })
            except ValueError:
                raise ValueError(param_key, 'параметр не найден')
        return result


class CardsAdsCountConverter:

    def convert(self, json_string: str) -> int:
        json_string = json_string.replace('for (;;);', '')
        data = json.loads(json_string)
        return data['payload']['totalCount']
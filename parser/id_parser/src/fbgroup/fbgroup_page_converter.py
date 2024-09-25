from .dto import FbGroup
from ..exceptions import HtmlElementNotFound

class PageConverter:

    def convert(self, html: str) -> FbGroup:
        string_to_search = '"delegate_page":{"id":"'
        start = html.find(string_to_search)
        if start != -1:
            end = html.find('"', start + len(string_to_search))
            group_id = html[start + len(string_to_search):end]
            return FbGroup(group_id=group_id)
        raise HtmlElementNotFound('delegate_page not found')
from .dto import FbGroup
from id_parser.src.exceptions import HtmlElementNotFound
import re
from common.utils import convert_to_int


class PageConverter:

    def convert(self, html: str) -> FbGroup:
        delegate_id = self.__get_delegate_id(html=html)
        likes_count = self.__get_likes_count(html=html)
        followers_count = self.__get_followers(html=html)
        return FbGroup(
            group_id=delegate_id,
            likes_count=likes_count,
            followers_count=followers_count,
        )

    def __get_delegate_id(self, html: str) -> str:
        string_to_search = '"delegate_page":{"id":"'
        start = html.find(string_to_search)
        if start != -1:
            end = html.find('"', start + len(string_to_search))
            return html[start + len(string_to_search):end]
        raise HtmlElementNotFound('delegate_page not found')

    def __get_followers(self, html: str):
        res = re.search(r'"text":"[\d.]{1,6}[KkMm]? followers"', html)
        if res:
            followers_string = res.group(0)
            for string in ('"text":"', '"', 'followers'):
                followers_string = followers_string.replace(string, '')
            followers_string = followers_string.strip()
            return convert_to_int(string=followers_string)
        with open('x.html', 'w') as file:
            file.write(html)
        return HtmlElementNotFound('followers not found')

    def __get_likes_count(self, html: str) -> int | None:
        res = re.search(r'"text":"[\d.]{1,6}[KkMm]? likes"', html)
        if res:
            likes_string = res.group(0)
            for string in ('"text":"', '"', 'likes'):
                likes_string = likes_string.replace(string, '')
            likes_string = likes_string.strip()
            return convert_to_int(string=likes_string)
        with open('x.html', 'w') as file:
            file.write(html)
        return None



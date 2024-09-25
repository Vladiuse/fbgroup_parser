from .dto import FbGroup
from .fbgroup_page_converter import PageConverter
from ..request_sender import FbRequestRequestSender

class FbPageProvider:

    def __init__(self, converter: PageConverter, request_sender: FbRequestRequestSender):
        self.converter = converter
        self.request_sender = request_sender

    def provide(self, url: str) -> FbGroup:
        html = self.request_sender.get(url)
        return self.converter.convert(html=html)
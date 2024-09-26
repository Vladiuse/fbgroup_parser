import requests as req

class FbRequestRequestSender:


    def get(self,
            url: str,
            headers: dict | None = None,
            cookies: dict | None = None,
            ) -> str:
        kwargs = {}
        if headers:
            kwargs.update({
                'headers': headers,
            })
        if cookies:
            kwargs.update({
                'cookies': cookies,
            })
        res = req.get(url, **kwargs)
        res.raise_for_status()
        return res.text
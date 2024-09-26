from dataclasses import dataclass


@dataclass
class FbLibAuthData:
    headers: dict
    cookies: dict
    data: dict
    session_id: str
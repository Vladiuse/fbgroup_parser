from dataclasses import dataclass



@dataclass
class FbGroup:
    group_id: str
    likes_count: int | None
    followers_count: int
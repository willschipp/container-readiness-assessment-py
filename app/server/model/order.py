from dataclasses import dataclass
from typing import List

from .job import Job

@dataclass
class Order:
    user_id: str
    app_id: str
    order_id: str
    job: Job
    files: List[str]
    finished: bool

    @classmethod
    def from_dict(cls, data):
        return cls(
            user_id = data.get('user_id'),
            app_id = data.get('app_id'),
            order_id = data.get('order_id')
        )    
from dataclasses import dataclass

from .form import Form

@dataclass
class Job:
    order_id: str
    current_step: int
    form: Form

    @classmethod
    def from_dict(cls, data):
        return cls(
            order_id = data.get('order_id'),
            current_step = data.get('current_step'),
            form = data.get('form')
        )
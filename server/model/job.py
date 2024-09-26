from dataclasses import dataclass

from .form import Form

@dataclass
class Job:
    orderid: str
    currentStep: int
    form: Form

    @classmethod
    def from_dict(cls, data):
        return cls(
            orderid = data.get('orderid'),
            currentStep = data.get('currentStep'),
            form = data.get('form')
        )
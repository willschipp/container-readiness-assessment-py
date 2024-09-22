from dataclasses import dataclass

from .form import Form

@dataclass
class Job:
    orderid: str
    currentStep: int
    form: Form
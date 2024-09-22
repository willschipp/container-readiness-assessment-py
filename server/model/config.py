from dataclasses import dataclass
from typing import List

from .applanguage import AppLanguage

@dataclass
class Config:
    updated: str
    languages: List[AppLanguage]
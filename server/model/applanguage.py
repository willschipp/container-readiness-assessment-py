from dataclasses import dataclass
from typing import List

from .prompt import Prompt

@dataclass
class AppLanguage:
    name: str
    prompts: List[Prompt]

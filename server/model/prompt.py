from dataclasses import dataclass
import os
import json

@dataclass
class Prompt:
    appLanguage: str
    prompt: str
    step: int

    @classmethod
    def from_dict(cls, data):
        return cls(
            appLanguage = data.get('appLanguage'),
            prompt = data.get('prompt'),
            step = data.get('step')
        )

   
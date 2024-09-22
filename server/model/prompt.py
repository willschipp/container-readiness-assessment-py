from dataclasses import dataclass

@dataclass
class Prompt:
    appLanguage: str
    prompt: str
    step: int
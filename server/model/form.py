from dataclasses import dataclass

@dataclass
class Form:
    userid: str
    appid: str
    applanguage: str
    configtext: str
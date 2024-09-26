from dataclasses import dataclass

@dataclass
class Form:
    userid: str
    appid: str
    applanguage: str
    configtext: str

    @classmethod
    def from_dict(cls, data):
        return cls(
            userid = data.get('userid'),
            appid = data.get('appid'),
            applanguage = data.get('applanguage'),
            configtext = data.get('configtext')
        )
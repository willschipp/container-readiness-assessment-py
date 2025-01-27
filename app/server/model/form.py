from dataclasses import dataclass

@dataclass
class Form:
    user_id: str
    app_id: str
    app_language: str
    config_text: str

    @classmethod
    def from_dict(cls, data):
        return cls(
            user_id = data.get('user_id'),
            app_id = data.get('app_id'),
            app_language = data.get('app_language'),
            config_text = data.get('config_text')
        )
from dataclasses import dataclass, asdict
import json

@dataclass
class Prompt:
    app_language: str
    prompt: str
    step: int

    @classmethod
    def from_dict(cls, data):
        return cls(
            app_language = data.get('app_language'),
            prompt = data.get('prompt'),
            step = data.get('step')
        )
    
    def to_dict(self):
        return asdict(self)   

    def to_json(self):
        return json.dumps(self.to_dict())        

   
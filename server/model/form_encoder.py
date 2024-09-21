from json import JSONEncoder

from .form import Form

class FormEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj,(Form)):
            return obj.__dict__
        return super().default(obj)
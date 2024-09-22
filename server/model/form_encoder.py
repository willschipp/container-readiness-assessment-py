from json import JSONEncoder

from .form import Form
from .applanguage import AppLanguage
from .config import Config
from .job import Job
from .order import Order
from .prompt import Prompt
from .response import GeminiReponse

class FormEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj,(Form,AppLanguage,Config,Job,Order,Prompt,GeminiReponse)):
            return obj.__dict__
        return super().default(obj)
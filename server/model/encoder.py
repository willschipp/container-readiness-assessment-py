from json import JSONEncoder, load
import os


from .form import Form
from .applanguage import AppLanguage
from .config import Config
from .job import Job
from .order import Order
from .prompt import Prompt
from .response import GeminiReponse

class Encoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj,(Form,AppLanguage,Config,Job,Order,Prompt,GeminiReponse)):
            return obj.__dict__
        return super().default(obj)
    

# helper function
def loadPrompts(): # TODO have location passed as a variable
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir,'./prompts.json')
    with open(file_path,'r') as prompt_file:
        data = load(prompt_file)

    prompts = []
    # iterate over the data to create multiple prompt objects
    for obj in data['prompts']:
        prompt = Prompt.from_dict(obj)
        prompts.append(prompt)
    return prompts
    
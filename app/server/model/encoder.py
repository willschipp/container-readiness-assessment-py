from json import JSONEncoder, load, dumps
import os


from .form import Form
from .applanguage import AppLanguage
from .config import Config
from .job import Job
from .order import Order
from .prompt import Prompt
from .response import GeminiResponse

class Encoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj,(Form,AppLanguage,Config,Job,Order,Prompt,GeminiResponse)):
            return obj.__dict__
        return super().default(obj)
    

# helper function
def load_prompts(): # TODO have location passed as a variable
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # file_path = os.path.join(current_dir,'./prompts.json')
    file_path = os.path.join(current_dir,'./prompts_codellama.json')
    with open(file_path,'r') as prompt_file:
        data = load(prompt_file)

    prompts = []
    # iterate over the data to create multiple prompt objects
    for obj in data['prompts']:
        prompt = Prompt.from_dict(obj)
        prompts.append(prompt)
    return prompts

   
def class_to_json(obj):
    def serialize(val):
        if isinstance(val, (int, float, str, bool, type(None))):
            return val
        elif isinstance(val, (list, tuple)):
            return [serialize(item) for item in val]
        elif isinstance(val, dict):
            return {str(k): serialize(v) for k, v in val.items()}
        elif hasattr(val, '__dict__'):
            return serialize(val.__dict__)
        else:
            return str(val)
    
    serialized_dict = serialize(obj.__dict__)
    return dumps(serialized_dict, indent=2)    
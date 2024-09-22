import uuid
import tempfile
import json
import os

from ..model.form import Form
from ..model.job import Job
from ..model.form_encoder import FormEncoder

from ..service.s3 import save

from ..config import config

def createJob(form: Form) -> str:
    # create a job object
    orderid = str(uuid.uuid4()).replace('-','')
    job = Job(
        orderid=orderid,
        currentStep=0,
        form=form
    )
    # persist job object by writing it out to json
    with tempfile.NamedTemporaryFile(mode="w+",delete=False,suffix=".json") as temp_file:
        json_string = json.dumps(job,cls=FormEncoder)
        temp_file.write(json_string)
        temp_file_path = temp_file.name
    
    # file is written --> save
    current_config = config['dev']

    save(temp_file_path,orderid,"job.json",current_config.URL,current_config.KEY,current_config.SECRET)

    # clean up the file
    os.remove(temp_file_path)

    return orderid

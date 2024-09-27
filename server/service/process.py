import uuid
import tempfile
import json
import os

import threading
import time

from ..model.form import Form
from ..model.job import Job
from ..model.encoder import Encoder, load_prompts

from ..service.s3 import save_file, list_files, get_buckets, get_file
from ..service.llm import call_gemini, clean_string

from ..config import config

# globals
prompts = []

def load():
    global prompts
    if len(prompts) <= 0:
        print("prompts loaded")
        prompts = load_prompts()


def create_job(form: Form) -> str:
    # create a job object
    order_id = str(uuid.uuid4()).replace('-','')
    job = Job(
        order_id=order_id,
        current_step=0,
        form=form
    )
    # persist job object by writing it out to json
    with tempfile.NamedTemporaryFile(mode="w+",delete=False,suffix=".json") as temp_file:
        json_string = json.dumps(job,cls=Encoder)
        temp_file.write(json_string)
        temp_file_path = temp_file.name
    
    # file is written --> save
    current_config = config['dev']

    save_file(temp_file_path,order_id,"job.json",current_config.URL,current_config.KEY,current_config.SECRET)

    # clean up the file
    os.remove(temp_file_path)

    return order_id

def step_is_self_contained(job: Job):
    # load up the prompts
    load()    
    # determine if the application is self-contained
    print("self contained ",job) # TODO fix for overall logging
    # get the config text
    config_text = clean_string(job.form.config_text)
    # get the prompts
    for p in prompts:
        print(p)
        if p.step == 0:
            # use this one
            # prompt_string = p.prompt + ' ' + job.form.configtext # add a string gap            
            prompt_string = p.prompt + ' ' + config_text # add a string gap            
            break          

    # send to the LLM
    result = call_gemini(prompt_string)
    # now parse the string
    # if it has 'yes' --> increment the step in the job to '1'
    # if it doesn't --> increment the step to '5' (exit out)
    # update the job outcome
    return

def step_create_dockerfile(job: Job):
    # create a dockerfile for it
    print("self dockerfile ",job)
    pass

def step_create_deployment_yaml(job: Job):
    # create a deployment yaml for the application
    print("self deployment ",job)
    pass

def step_create_service_yaml(job: Job):
    # create the service yaml for the application
    print("self service ",job)
    pass

def step_finished_job(job: Job):
    # create the "finished.json" file and write it back
    with tempfile.NamedTemporaryFile(mode="w+",delete=False,suffix=".json") as temp_file:
        temp_file.write('')
        temp_file_path = temp_file.name
    
    # file is written --> save
    current_config = config['dev']
    save_file(temp_file_path,job.order_id,"finished.json",current_config.URL,current_config.KEY,current_config.SECRET)
    # clean up the file
    os.remove(temp_file_path)
    return

def process_job(job: Job):
    # retrieve the current step
    currentStep = job.current_step
    switcher = {
        0: step_is_self_contained,
        1: step_create_dockerfile,
        2: step_create_deployment_yaml,
        3: step_create_service_yaml
    }
    return switcher.get(currentStep,step_finished_job)(job)

def find_active_jobs():
    #config
    current_config = config['dev']

    bucket_names = get_buckets(current_config.URL,current_config.KEY,current_config.SECRET)
    for bucket_name in bucket_names:
        finished = False
        # get all the files
        file_names = list_files(bucket_name,current_config.URL,current_config.KEY,current_config.SECRET)
        for file_name in file_names:
            # first check for 'finished.json'
            if file_name == 'finished.json':
                # done
                finished = True
                break
        
        if finished == False:
            # retrieve the job
            with tempfile.NamedTemporaryFile(mode="w+",delete=False,suffix=".json") as temp_file:
                pass
            get_file(temp_file.name,bucket_name,"job.json",current_config.URL,current_config.KEY,current_config.SECRET)
            # read into json
            with open(temp_file.name,'r') as job_file:
                data = json.load(job_file)
            job = Job.from_dict(data)
            # clean up
            os.remove(temp_file.name)
            # process job
            process_job(job)        

def background_process():
    while True:
        # run
        find_active_jobs()
        # now pause
        time.sleep(5)

def start_background():
    bg_thread = threading.Thread(target=background_process)
    bg_thread.daemon = True
    bg_thread.start()



import json
import logging
import os
import tempfile
import threading
import time
import uuid

from ..model.form import Form
from ..model.job import Job
from ..model.response import parse_json_to_gemini_response
from ..model.encoder import Encoder, load_prompts

from ..service.s3 import save_file, list_files, get_buckets, get_file
from ..service.llm import clean_string, call_llm
from ..service.file_formatter import convert_to_dockerfile, convert_to_yaml

from ..config import config
from ..logging_config import setup_logging

# globals
prompts = []

llm_name = ""

logger = setup_logging()

def load():
    global prompts
    global llm_name
    if len(prompts) <= 0:
        logger.info("prompts loaded")
        prompts = load_prompts()
        # load the environment
        llm_name = os.getenv('RUN_MODE','dev')

def parse_response(reply: str):
    if llm_name == "ollama":
        logger.info("parsing ollama response")
        data = json.loads(reply)
        return data.get("response",None)
    elif llm_name == "dev":
        logger.info("parsing gemini response")
        # parse gemini
        response = parse_json_to_gemini_response(reply)
        return response.candidates[0].content.parts[0].text #location of the detailed response
    else:
        logger.info("parsing other response")
        # parse 'content'
        data = json.loads(reply)
        return data.get("content",None)


def save_string(content: str,bucket_name: str,obj_name: str):
    # persist job object by writing it out to json
    with tempfile.NamedTemporaryFile(mode="w+",delete=False,suffix=".json") as temp_file:
        temp_file.write(content)
        temp_file_path = temp_file.name

    # file is written --> save
    current_config = config[os.getenv('RUN_MODE','dev')]

    save_file(temp_file_path,bucket_name,obj_name,current_config.URL,current_config.KEY,current_config.SECRET)

    logger.info(f"file {obj_name} saved")
    # clean up the file
    os.remove(temp_file_path)


def create_job(form: Form) -> str:
    # create a job object
    order_id = str(uuid.uuid4()).replace('-','')
    job = Job(
        order_id=order_id,
        current_step=0,
        form=form
    )
    # persist job object by writing it out to json
    json_string = json.dumps(job,cls=Encoder)
    # save it
    save_string(json_string,order_id,"job.json")
    # log
    logger.info(f"job {job.order_id} created and saved")
    # start thread
    start_background()    
    # return
    return order_id

def step_is_self_contained(job: Job):
    # load up the prompts
    load()    
    # determine if the application is self-contained
    logger.debug(f"self contained {job}")
    # get the config text
    config_text = clean_string(job.form.config_text)
    # get the prompts
    for p in prompts:
        if p.step == 0:
            # use this one
            prompt_string = p.prompt + ' ' + config_text # add a string gap            
            break          

    # send to the LLM
    try:
        # result = call_gemini(prompt_string)
        result = call_llm(prompt_string,llm_name)
        # now parse the string
        logger.debug(f"result {result}")
        # parse into the response
        # response = parse_json_to_gemini_response(result)
        # answer = response.candidates[0].content.parts[0].text #location of the detailed response
        answer = parse_response(result)
        # save the answer
        save_string(result,job.order_id,"answer_0.json")
        # if it has 'yes' --> increment the step in the job to '1'
        if 'yes'.lower() in answer.lower():
            # update the job to step 1
            job.current_step = 1
            # save the job
            json_string = json.dumps(job,cls=Encoder)
            save_string(json_string,job.order_id,"job.json")
            # log it
            logger.info(f"job {job.order_id} updated and saved")
        else:
            # if it doesn't --> increment the step to '5' (exit out)
            # update the job outcome
            logger.info("Not able to containerize")
            logger.debug(f"response {answer} for {job}")
            step_finished_job(job)
        return
    except Exception as err:
        logger.error(f"error occurred - halted {err}")
        return

def step_create_dockerfile(job: Job):
    # create a dockerfile for it
    #TODO include application logic choices
    # load up the prompts
    load()    
    # determine if the application is self-contained
    logger.debug(f"dockerfile creation {job}")
    # get the config text
    config_text = clean_string(job.form.config_text)
    # get the prompts
    for p in prompts:
        if p.step == 1:
            # use this one
            prompt_string = p.prompt + ' ' + config_text # add a string gap            
            break          

    # send to the LLM
    result = call_llm(prompt_string,llm_name)
    # now parse the string
    logger.debug(f"result {result}")
    # save the answer
    save_string(result,job.order_id,"answer_1.json")
    # get the answer and write it out as a docker file
    # response = parse_json_to_gemini_response(result)
    # answer = response.candidates[0].content.parts[0].text 
    answer = parse_response(result)
    docker_file = convert_to_dockerfile(answer)
    save_string(docker_file,job.order_id,"Dockerfile")
    # update the job to step 2
    job.current_step = 2
    # save the job
    json_string = json.dumps(job,cls=Encoder)
    save_string(json_string,job.order_id,"job.json")
    # log it
    logger.info(f"job {job.order_id} updated and saved")


def step_create_deployment_yaml(job: Job):
    # create a deployment yaml for the application
    # load up the prompts
    load()    
    # determine if the application is self-contained
    logger.debug(f"deployment yaml creation {job}")
    # get the config text
    config_text = clean_string(job.form.config_text)
    # get the prompts
    for p in prompts:
        if p.step == 2:
            # use this one
            prompt_string = p.prompt + ' ' + config_text # add a string gap            
            break          

    # send to the LLM
    result = call_llm(prompt_string,llm_name)
    # now parse the string
    logger.debug(f"result {result}")
    # save the answer
    save_string(result,job.order_id,"answer_2.json")

    # response = parse_json_to_gemini_response(result)
    # answer = response.candidates[0].content.parts[0].text 
    answer = parse_response(result)
    deployment_yaml = convert_to_yaml(answer)
    save_string(deployment_yaml,job.order_id,"deployment.yaml")
    # update the job to step 3
    job.current_step = 3
    # save the job
    json_string = json.dumps(job,cls=Encoder)
    save_string(json_string,job.order_id,"job.json")

    logger.info(f"job {job.order_id} updated and saved")

def step_create_service_yaml(job: Job):
    # create the service yaml for the application
    # load up the prompts
    load()    
    # determine if the application is self-contained
    logger.debug(f"service yaml creation {job}")
    # get the config text
    config_text = clean_string(job.form.config_text)
    # get the prompts
    for p in prompts:
        if p.step == 3:
            # use this one
            prompt_string = p.prompt + ' ' + config_text # add a string gap            
            break          

    # send to the LLM
    result = call_llm(prompt_string,llm_name)
    # now parse the string
    logger.debug(f"result {result}")
    # save the answer
    save_string(result,job.order_id,"answer_3.json")

    # response = parse_json_to_gemini_response(result)
    # answer = response.candidates[0].content.parts[0].text 
    answer = parse_response(result)
    service_yaml = convert_to_yaml(answer)
    save_string(service_yaml,job.order_id,"service.yaml")

    # update the job to step 4 (finished)
    job.current_step = 4
    # save the job
    json_string = json.dumps(job,cls=Encoder)
    save_string(json_string,job.order_id,"job.json")

    logger.info(f"job {job.order_id} updated and saved")
    # directly invoke close out
    step_finished_job(job)

def step_finished_job(job: Job):
    # create the "finished.json" file and write it back
    save_string("",job.order_id,"finished.json")

    logger.info(f"job {job.order_id} finished")
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
    current_config = config[os.getenv('RUN_MODE','dev')]

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

#TODO handle exception in threads

def start_background():
    for th in threading.enumerate():
        if th.name == "processing_thread":
            logger.info("thread still running")
            break
    else:
        bg_thread = threading.Thread(target=background_process,name="processing_thread")
        bg_thread.daemon = True
        bg_thread.start()



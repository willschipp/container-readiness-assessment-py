import json
import logging
import os
import tempfile
import threading
import time
import uuid
from loguru import logger

from server.configuration import settings
import server.constants as constants

from server.model.form import Form
from server.model.job import Job
from server.model.response import parse_json_to_gemini_response
from server.model.encoder import Encoder, load_prompts

from server.service.s3 import list_folders, get_file_from_folder, put_file_to_folder, is_file_in_folder
from server.service.llm import clean_string, call_llm
from server.service.file_formatter import convert_to_dockerfile, convert_to_yaml


# globals
prompts = []


def load():
    global prompts
    if len(prompts) <= 0:
        logger.info("prompts loaded")
        prompts = load_prompts()

# support reloading
def reset_prompts(location):
    global prompts
    prompts = load_prompts(location)

def get_prompts():
    load()
    return prompts

def parse_response(reply: str):
    if settings.llm_name == constants.LLM_NAME_OLLAMA:
        logger.info("parsing ollama response")
        data = json.loads(reply)
        return data.get("response",None)
    elif settings.llm_name == constants.LLM_NAME_GEMINI:
        logger.info("parsing gemini response")
        # parse gemini
        response = parse_json_to_gemini_response(reply)
        return response.candidates[0].content.parts[0].text #location of the detailed response
    else:
        # llama cpp default
        logger.info("parsing llamacpp response")
        # parse 'content'
        data = json.loads(reply)
        return data.get("content",None)


def save_string(content: str,folder_name: str,obj_name: str):
    # persist job object by writing it out to json
    with tempfile.NamedTemporaryFile(mode="w+",delete=False,suffix=".json") as temp_file:
        temp_file.write(content)
        temp_file_path = temp_file.name

    # file is written --> save
    # current_config = config[os.getenv('RUN_MODE','dev')]

    # save_file(temp_file_path,bucket_name,obj_name,current_config.URL,current_config.KEY,current_config.SECRET)
    # save_file_in_folder(temp_file_path, folder_name, bucket_name, obj_name, current_config.URL,current_config.KEY,current_config.SECRET)
    put_file_to_folder(temp_file_path,folder_name,obj_name)

    logger.info(f"file {obj_name} saved")
    # clean up the file
    os.remove(temp_file_path)


def create_job(form: Form) -> str:
    # create a job object
    order_id = str(uuid.uuid4()).replace('-','')
    job = Job(
        order_id=order_id,
        current_step=0,
        form=form,
        result=-1
    )
    # persist job object by writing it out to json
    json_string = json.dumps(job,cls=Encoder)
    # save it
    save_string(json_string,order_id,constants.FILE_NAME_JOB)
    # log
    logger.info(f"job {job.order_id} created and saved")
    # start thread
    start_background()    
    # return
    return order_id


def step_get_language(job: Job):
    # load up the prompts
    load()    
    # determine if the application is self-contained
    logger.debug(f"get language {job}")
    # get the config text
    config_text = clean_string(job.form.config_text)
    # get the prompts
    for p in prompts:
        if p.step == -1:
            # use this one
            prompt_string = p.prompt + ' ' + config_text # add a string gap            
            break          

    # send to the LLM
    try:
        # result = call_gemini(prompt_string)
        result = call_llm(prompt_string,settings.llm_name)
        # now parse the string
        logger.debug(f"result {result}")
        # parse into the response
        # response = parse_json_to_gemini_response(result)
        # answer = response.candidates[0].content.parts[0].text #location of the detailed response
        answer = parse_response(result)
        # save the answer
        save_string(result,job.order_id,"answer_0.json")

        # the 'answer' is the language
        logger.debug(f"answer {answer}")

        # add to the job
        job.form.app_language = answer.lower()
        job.current_step = 1

        # save the job
        json_string = json.dumps(job,cls=Encoder)
        save_string(json_string,job.order_id,constants.FILE_NAME_JOB)
        # log it
        logger.info(f"job {job.order_id} updated and saved")

        return
    except Exception as err:
        logger.error(f"error occurred - halted {err}")
        return

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
        result = call_llm(prompt_string,settings.llm_name)
        # now parse the string
        logger.debug(f"result {result}")
        # parse into the response
        # response = parse_json_to_gemini_response(result)
        # answer = response.candidates[0].content.parts[0].text #location of the detailed response
        answer = parse_response(result)
        # save the answer
        save_string(result,job.order_id,"answer_1.json")
        # if it has 'yes' --> increment the step in the job to '1'
        if 'yes'.lower() in answer.lower():
            # update the job to step 2
            job.current_step = 2
            # set the results
            job.result = 1
            # save the job
            json_string = json.dumps(job,cls=Encoder)
            save_string(json_string,job.order_id,constants.FILE_NAME_JOB)
            # log it
            logger.info(f"job {job.order_id} updated and saved")
        else:
            # if it doesn't --> increment the step to '5' (exit out)
            # update the job outcome
            logger.info("Not able to containerize")
            logger.debug(f"response {answer} for {job}")
            job.result = 0
            step_finished_job(job)
        return
    except Exception as err:
        logger.error(f"error occurred - halted {err}")
        return


def step_create_dockerfile(job: Job):
    # create a dockerfile for it
    #TODO include application logic choices
    language = job.form.app_language
    # load up the prompts
    load()    
    # determine if the application is self-contained
    logger.debug(f"dockerfile creation {job}")
    # get the config text
    config_text = clean_string(job.form.config_text)
    # base
    prompt_string = ""
    # get the prompts
    for p in prompts:
        # if p.step == 1 and p.app_language == language:
        if p.step == 1 and p.app_language == 'any':
            # use this one
            prompt_string = p.prompt + ' ' + config_text # add a string gap            
            break          

    # send to the LLM
    result = call_llm(prompt_string,settings.llm_name)
    # now parse the string
    logger.debug(f"result {result}")
    # save the answer
    save_string(result,job.order_id,"answer_2.json")
    # get the answer and write it out as a docker file
    # response = parse_json_to_gemini_response(result)
    # answer = response.candidates[0].content.parts[0].text 
    answer = parse_response(result)
    try:
        docker_file = convert_to_dockerfile(answer)
        save_string(docker_file,job.order_id,"Dockerfile")
    except Exception as err:
        logger.error(f"error occurred parsing dockerfile - continuing: {err}")
    # update the job to step 2
    job.current_step = 3
    # save the job
    json_string = json.dumps(job,cls=Encoder)
    save_string(json_string,job.order_id,constants.FILE_NAME_JOB)
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
    result = call_llm(prompt_string,settings.llm_name)
    # now parse the string
    logger.debug(f"result {result}")
    # save the answer
    save_string(result,job.order_id,"answer_3.json")

    # response = parse_json_to_gemini_response(result)
    # answer = response.candidates[0].content.parts[0].text 
    answer = parse_response(result)
    try:
        deployment_yaml = convert_to_yaml(answer)
        save_string(deployment_yaml,job.order_id,"deployment.yaml")
    except Exception as err:
        logger.error(f"error occurred parsing deployment yaml - continuing: {err}")
    # update the job to step 3
    job.current_step = 4
    # save the job
    json_string = json.dumps(job,cls=Encoder)
    save_string(json_string,job.order_id,constants.FILE_NAME_JOB)

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
    result = call_llm(prompt_string,settings.llm_name)
    # now parse the string
    logger.debug(f"result {result}")
    # save the answer
    save_string(result,job.order_id,"answer_4.json")

    # response = parse_json_to_gemini_response(result)
    # answer = response.candidates[0].content.parts[0].text 
    answer = parse_response(result)
    try:
        service_yaml = convert_to_yaml(answer)
        save_string(service_yaml,job.order_id,"service.yaml")
    except Exception as err:
        logger.error(f"error occurred parsing service yaml - continuing: {err}")
    # update the job to step 4 (finished)
    job.current_step = 5
    # save the job
    json_string = json.dumps(job,cls=Encoder)
    save_string(json_string,job.order_id,constants.FILE_NAME_JOB)

    logger.info(f"job {job.order_id} updated and saved")
    # directly invoke close out
    step_finished_job(job)

def step_finished_job(job: Job):
    # create the "finished.json" file and write it back
    save_string("",job.order_id,constants.FILE_NAME_FINISHED)
    # finished
    logger.info(f"job {job.order_id} finished")
    return



def process_job(job: Job):
    # retrieve the current step
    currentStep = job.current_step
    switcher = {
        0: step_get_language,
        1: step_is_self_contained,
        2: step_create_dockerfile,
        3: step_create_deployment_yaml,
        4: step_create_service_yaml
    }
    return switcher.get(currentStep,step_finished_job)(job)

def find_active_jobs():
    #config
    
    # bucket_names = get_buckets(current_config.URL,current_config.KEY,current_config.SECRET)

    # folder_names = get_folders(bucket_name,current_config.URL,current_config.KEY,current_config.SECRET)
    folder_names = list_folders()

    if type(folder_names) is list and len(folder_names) > 0:
        finished_count = 0

        # Folders in bucket
        for folder_name in folder_names:
            # Files in folder
            if not is_file_in_folder(folder_name, constants.FILE_NAME_FINISHED):
                logger.info(f"{folder_name} Process")

                # Retrieve job and process
                with tempfile.NamedTemporaryFile(
                    mode="w+", delete=False, suffix=".json"
                ) as temp_file:
                    # Empty file
                    pass
                get_file_from_folder(
                    folder_name, constants.FILE_NAME_JOB, temp_file.name
                )
                with open(temp_file.name, "r") as job_file:
                    job_content = json.load(job_file)
                os.remove(temp_file.name)

                # Process job
                process_job(Job.from_dict(job_content))
            else:
                finished_count += 1
                logger.info(f"{folder_name} Finished")

        logger.info(f"{finished_count} of {len(folder_names)} jobs finished")
        if finished_count == len(folder_names):
            return False
        else:
            return True
    else:
        logger.info("No jobs found")
        return False
       

def background_process():
    while True:
        # run
        find_active_jobs()
        # now pause
        time.sleep(5)

#TODO handle exception in threads

def start_background():
    logger.info("starting the backgorund process")
    for th in threading.enumerate():
        if th.name == "processing_thread":
            logger.info("thread still running")
            break
    else:
        bg_thread = threading.Thread(target=background_process,name="processing_thread")
        bg_thread.daemon = True
        bg_thread.start()



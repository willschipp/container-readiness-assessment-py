import uuid
import tempfile
import json
import os

import threading
import time

from ..model.form import Form
from ..model.job import Job
from ..model.form_encoder import FormEncoder

from ..service.s3 import save, listFiles, getBuckets, get

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

def isSelfContained(job: Job):
    # determine if the application is self-contained
    print("self contained ",job)
    pass

def createDockerfile(job: Job):
    # create a dockerfile for it
    print("self dockerfile ",job)
    pass

def createDeploymentYaml(job: Job):
    # create a deployment yaml for the application
    print("self deployment ",job)
    pass

def createServiceYaml(job: Job):
    # create the service yaml for the application
    print("self service ",job)
    pass

def noAction(job: Job):
    pass

def processJob(job: Job):
    # retrieve the current step
    currentStep = job.currentStep
    switcher = {
        0: isSelfContained,
        1: createDockerfile,
        2: createDeploymentYaml,
        3: createServiceYaml
    }
    return switcher.get(currentStep,noAction)(job)

def getActiveJobs():
    #config
    current_config = config['dev']

    bucket_names = getBuckets(current_config.URL,current_config.KEY,current_config.SECRET)
    for bucket_name in bucket_names:
        finished = False
        # get all the files
        file_names = listFiles(bucket_name,current_config.URL,current_config.KEY,current_config.SECRET)
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
            get(temp_file.name,bucket_name,"job.json",current_config.URL,current_config.KEY,current_config.SECRET)
            # read into json
            with open(temp_file.name,'r') as job_file:
                data = json.load(job_file)
            job = Job.from_dict(data)
            # clean up
            os.remove(temp_file.name)
            # process job
            processJob(job)        


def background_process():
    while True:
        # get all the buckets from s3
        # for each bucket, check for "finished.json"
        # if doesn't exist, retrieve the job.json
        # pass it to processjob
        getActiveJobs()
        # now pause
        time.sleep(5)

def start_background():
    bg_thread = threading.Thread(target=background_process)
    bg_thread.daemon = True
    bg_thread.start()



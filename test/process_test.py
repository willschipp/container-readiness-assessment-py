import unittest

import os
import tempfile
import threading
import time
import uuid

from server.model.form import Form
from server.model.job import Job
from server.service.process import create_job, process_job, start_background, step_is_self_contained, step_finished_job, step_create_dockerfile
from server.service.s3 import create_bucket, list_files, clean_up, get_file

class TestProcess(unittest.TestCase):

    def setUp(self):
        self.secret = os.getenv("SECRET")
        self.url = "localhost:9000"
        self.key = "gjUHI2lScQ6JhwnbBkas"

    def tearDown(self):
        clean_up(self.url,self.key,self.secret)        


    # def test_createJob(self):
    #     # create a form
    #     form = Form(
    #         userid="jdoe",
    #         appid="1234",
    #         applanguage="java",
    #         configtext="blah blah blah"
    #     )
    #     # submit to the create job process and get back an orderid
    #     orderid = createJob(form)
    #     self.assertIsNotNone(orderid)

    # def test_processJob(self):
    #     # create form
    #     form = Form(
    #         userid="jdoe",
    #         appid="1234",
    #         applanguage="java",
    #         configtext="blah blah blah"
    #     )
    #     # create job
    #     job = Job(
    #         orderid="1234",
    #         currentStep=0,
    #         form=form
    #     )
    #     # execute
    #     processJob(job)

    # def test_backgroundProcess(self):
    #     # start the process
    #     startBackground()
    #     time.sleep(0.1)
    #     # check
    #     threads = threading.enumerate()
    #     background_threads = [t for t in threads if t.name == 'Thread-1']
    #     self.assertEqual(len(background_threads),1)
    #     self.assertTrue(background_threads[0].is_alive())
    #     pass

    # def test_isSelfContained(self):
    #     # create the form
    #     form = Form(
    #         userid="jdoe",
    #         appid="1234",
    #         applanguage="java",
    #         configtext="blah blah blah"
    #     )
    #     # create the job object
    #     job = Job(
    #         orderid="1234",
    #         currentStep=0,
    #         form=form
    #     )
    #     # execute
    #     isSelfContained(job)

    # def test_noAction(self):
    #     # create a bucket called 1234
    #     bucketname = str(uuid.uuid4()).replace('-','')
    #     create_bucket(bucketname,self.url,self.key,self.secret)
    #     # create a form
    #     form = Form(
    #         user_id="jdoe",
    #         app_id="1234",
    #         app_language="java",
    #         config_text="blah blah blah"
    #     )        
    #     # create job
    #     job = Job(
    #         order_id=bucketname,
    #         current_step=0,
    #         form=form
    #     )
    #     # invoke
    #     step_finished_job(job)
    #     # now check if there's a "finished.json" in the bucket
    #     has_file = False
    #     files = list_files(bucketname,self.url,self.key,self.secret)
    #     for file in files:
    #         if file == "finished.json":
    #             has_file = True
    #             break
    #     self.assertTrue(has_file)

    # def test_step_is_self_contained(self):
    #     #load up the sameple data 
    #     current_dir = os.path.dirname(os.path.abspath(__file__))
    #     file_path = os.path.join(current_dir,'./examples/spring_boot_build.gradle')
    #     # load up the file
    #     with open(file_path,'r') as input:
    #         content = input.read()

    #     bucketname = str(uuid.uuid4()).replace('-','')
    #     create_bucket(bucketname,self.url,self.key,self.secret)

    #     form = Form(
    #         user_id="jdoe",
    #         app_id="1234",
    #         app_language="java",
    #         config_text=content
    #     )    
    #     # create job
    #     job = Job(
    #         order_id=bucketname,
    #         current_step=0,
    #         form=form
    #     )            
    #     # now invoke
    #     step_is_self_contained(job)
    #     # check if the file exists
    #     has_file = False
    #     files = list_files(bucketname,self.url,self.key,self.secret)
    #     for file in files:
    #         if file == "answer_0.json":
    #             has_file = True
    #             break
    #     self.assertTrue(has_file)

    # def test_step_create_dockerfile(self):
    #     current_dir = os.path.dirname(os.path.abspath(__file__))
    #     file_path = os.path.join(current_dir,'./examples/spring_boot_build.gradle')
    #     # load up the file
    #     with open(file_path,'r') as input:
    #         content = input.read()

    #     bucketname = str(uuid.uuid4()).replace('-','')
    #     create_bucket(bucketname,self.url,self.key,self.secret)

    #     form = Form(
    #         user_id="jdoe",
    #         app_id="1234",
    #         app_language="java",
    #         config_text=content
    #     )    
    #     # create job
    #     job = Job(
    #         order_id=bucketname,
    #         current_step=1,
    #         form=form
    #     )     
    #     step_create_dockerfile(job)     
    #     # check if the file exists
    #     has_file = False
    #     files = list_files(bucketname,self.url,self.key,self.secret)
    #     for file in files:
    #         if file == "answer_1.json":
    #             has_file = True
    #             break
    #     self.assertTrue(has_file)
    #     #retrieve the file
    #     with tempfile.NamedTemporaryFile(mode="w+",delete=False,suffix=".json") as temp_file:
    #         pass
    #     get_file(temp_file.name,bucketname,"answer_1.json",self.url,self.key,self.secret)
    #     with open(temp_file.name,'r') as file:
    #         content = file.read()
    #     self.assertTrue(len(content) > 0)
    #     print(content)

    #     os.remove(temp_file.name)        
        
    def test_process_job_full(self):
        # create a job and walk it through the steps 5 times
        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_dir,'./examples/spring_boot_build.gradle')
        # load up the file
        with open(file_path,'r') as input:
            content = input.read()

        bucketname = str(uuid.uuid4()).replace('-','')
        create_bucket(bucketname,self.url,self.key,self.secret)

        form = Form(
            user_id="jdoe",
            app_id="1234",
            app_language="java",
            config_text=content
        )    
        # create job
        job = Job(
            order_id=bucketname,
            current_step=0,
            form=form
        )     
        # iteration 0
        process_job(job)
        
        # check for answer 0
        # check if the file exists
        has_file = False
        files = list_files(bucketname,self.url,self.key,self.secret)
        for file in files:
            if file == "answer_0.json":
                has_file = True
                break
        self.assertTrue(has_file)
        # iteration 1
        time.sleep(3)
        process_job(job)
        # check for answer 1
        # check if the file exists
        has_file = False
        files = list_files(bucketname,self.url,self.key,self.secret)
        for file in files:
            if file == "answer_1.json":
                has_file = True
                break
        self.assertTrue(has_file)
        # iteration 2
        time.sleep(3)
        process_job(job)
        # check for answer 2
        # check if the file exists
        has_file = False
        files = list_files(bucketname,self.url,self.key,self.secret)
        for file in files:
            if file == "answer_2.yaml":
                has_file = True
                break
        self.assertTrue(has_file)
        # iteration 3
        time.sleep(3)
        process_job(job)
        # check for answer 3
        # check if the file exists
        has_file = False
        files = list_files(bucketname,self.url,self.key,self.secret)
        for file in files:
            if file == "answer_3.yaml":
                has_file = True
                break
        self.assertTrue(has_file)
        # iteration 4
        time.sleep(3)
        process_job(job)
        has_file = False
        files = list_files(bucketname,self.url,self.key,self.secret)
        for file in files:
            if file == "finished.json":
                has_file = True
                break
        self.assertTrue(has_file)






#TODO create "opposite" of 'yes' parse


if __name__ == '__main__':
    unittest.main()        
import unittest

import os
import threading
import time
import uuid

from server.model.form import Form
from server.model.job import Job
from server.service.process import create_job, process_job, start_background, step_is_self_contained, step_finished_job
from server.service.s3 import create_bucket, list_files, clean_up

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

    def test_noAction(self):
        # create a bucket called 1234
        bucketname = str(uuid.uuid4()).replace('-','')
        create_bucket(bucketname,self.url,self.key,self.secret)
        # create a form
        form = Form(
            user_id="jdoe",
            app_id="1234",
            app_language="java",
            config_text="blah blah blah"
        )        
        # create job
        job = Job(
            order_id=bucketname,
            current_step=0,
            form=form
        )
        # invoke
        step_finished_job(job)
        # now check if there's a "finished.json" in the bucket
        has_file = False
        files = list_files(bucketname,self.url,self.key,self.secret)
        for file in files:
            if file == "finished.json":
                has_file = True
                break
        self.assertTrue(has_file)



if __name__ == '__main__':
    unittest.main()        
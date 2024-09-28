import unittest
import json
import os
import uuid

from server.model.form import Form
from server.model.job import Job
from server.model.encoder import Encoder

class TestProcess(unittest.TestCase):

    def setUp(self):
        pass

    def test_from_dict(self):
        # create a job object and form

        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_dir,'./examples/spring_boot_build.gradle')
        # load up the file
        with open(file_path,'r') as input:
            content = input.read()
        
        order_id = str(uuid.uuid4()).replace('-','')
        
        form = Form(
            user_id="jdoe",
            app_id="1234",
            app_language="java",
            config_text=content
        )    
        # create job
        job = Job(
            order_id=order_id,
            current_step=0,
            form=form
        )  

        # write out a json object from it to a file
        json_str = json.dumps(job,cls=Encoder)
        # load up a json from it
        json_dict = json.loads(json_str)
        # recreate a job object from it
        job_recreate = Job.from_dict(json_dict)
        self.assertTrue(job_recreate.order_id == order_id)
        self.assertTrue(job_recreate.form.app_id == "1234")
        # pass

if __name__ == '__main__':
    unittest.main()          
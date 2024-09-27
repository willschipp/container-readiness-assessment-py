import unittest

import threading
import time

from server.model.form import Form
from server.model.job import Job
from server.service.process import createJob, processJob, startBackground, isSelfContained

class TestProcess(unittest.TestCase):

    def setUp(self):
        pass

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

    def test_isSelfContained(self):
        # create the form
        form = Form(
            userid="jdoe",
            appid="1234",
            applanguage="java",
            configtext="blah blah blah"
        )
        # create the job object
        job = Job(
            orderid="1234",
            currentStep=0,
            form=form
        )
        # execute
        isSelfContained(job)


if __name__ == '__main__':
    unittest.main()        
import unittest


from server.model.form import Form
from server.model.job import Job
from server.service.process import createJob, processJob

class TestProcess(unittest.TestCase):

    def setUp(self):
        pass

    def test_createJob(self):
        # create a form
        form = Form(
            userid="jdoe",
            appid="1234",
            applanguage="java",
            configtext="blah blah blah"
        )
        # submit to the create job process and get back an orderid
        orderid = createJob(form)
        self.assertIsNotNone(orderid)

    def test_processJob(self):
        # create form
        form = Form(
            userid="jdoe",
            appid="1234",
            applanguage="java",
            configtext="blah blah blah"
        )
        # create job
        job = Job(
            orderid="1234",
            currentStep=0,
            form=form
        )
        # execute
        processJob(job)


if __name__ == '__main__':
    unittest.main()        
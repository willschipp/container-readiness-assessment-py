import unittest


from server.model.form import Form
from server.service.process import createJob

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

if __name__ == '__main__':
    unittest.main()        
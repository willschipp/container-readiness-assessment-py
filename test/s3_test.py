import unittest
import os
import tempfile

from server.service.s3 import save

class TestS3(unittest.TestCase):

    def setUp(self):
        self.secret = os.getenv("SECRET")
        self.url = "localhost:9000"
        self.key = "gjUHI2lScQ6JhwnbBkas"

    def tearDown(self):
        os.remove(self.tempfile)


    def test_save(self):
        bucketname = "testbucket"
        with tempfile.NamedTemporaryFile(mode="w+",delete=False,suffix=".json") as temp_file:
            temp_file.write('{"hello":"world"}')
            temp_file_path = temp_file.name
        
        self.tempfile = temp_file_path #to clean up

        result = save(temp_file_path,bucketname,"test_obj",self.url,self.key,self.secret)
        print("result ",result)

        
if __name__ == '__main__':
    unittest.main()

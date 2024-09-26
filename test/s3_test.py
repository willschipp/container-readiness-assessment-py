import unittest
import os
import tempfile
import uuid

from server.service.s3 import save, getBuckets, listFiles, get

class TestS3(unittest.TestCase):

    def setUp(self):
        self.secret = os.getenv("SECRET")
        self.url = "localhost:9000"
        self.key = "gjUHI2lScQ6JhwnbBkas"

    def test_save(self):
        # bucketname = "testbucket"
        bucketname = str(uuid.uuid4()).replace('-','')
        with tempfile.NamedTemporaryFile(mode="w+",delete=False,suffix=".json") as temp_file:
            temp_file.write('{"hello":"world"}')
            temp_file_path = temp_file.name
        
        result = save(temp_file_path,bucketname,"test_obj",self.url,self.key,self.secret)
        print("result ",result)
        os.remove(temp_file_path)

    def test_getBuckets(self):
        buckets = getBuckets(self.url,self.key,self.secret)
        self.assertTrue(len(buckets) > 0)
        for bucket in buckets:
            print(bucket)

    def test_listFiles(self):
        buckets = getBuckets(self.url,self.key,self.secret)
        self.assertTrue(len(buckets) > 0)
        for bucket in buckets:
            files = listFiles(bucket,self.url,self.key,self.secret)
            for file in files:
                print(file)

    def test_get(self):
        # bucketname = "testbucket"
        bucketname = str(uuid.uuid4()).replace('-','')
        with tempfile.NamedTemporaryFile(mode="w+",delete=False,suffix=".json") as temp_file:
            temp_file.write('{"hello":"world"}')
            temp_file_path = temp_file.name
        
        result = save(temp_file_path,bucketname,"test_obj",self.url,self.key,self.secret)
        print("result ",result)
        os.remove(temp_file_path)
        # create a target temp file
        with tempfile.NamedTemporaryFile(mode="w+",delete=False,suffix=".json") as temp_file:
            pass
        get(temp_file_path,bucketname,"test_obj",self.url,self.key,self.secret)
        # now read the file
        with open(temp_file_path,'r') as file:
            content = file.read()
        print(content)
        os.remove(temp_file_path)


        
if __name__ == '__main__':
    unittest.main()

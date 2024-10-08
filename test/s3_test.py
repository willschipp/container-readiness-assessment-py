import unittest
import os
import tempfile
import uuid

from server.service.s3 import save_file, get_buckets, list_files, get_file, clean_up, create_bucket

class TestS3(unittest.TestCase):

    def setUp(self):
        self.secret = os.getenv("SECRET")
        self.url = "localhost:9000"
        self.key = "gjUHI2lScQ6JhwnbBkas"

    def tearDown(self):
        clean_up(self.url,self.key,self.secret)

    def test_save(self):
        # bucketname = "testbucket"
        bucketname = str(uuid.uuid4()).replace('-','')
        with tempfile.NamedTemporaryFile(mode="w+",delete=False,suffix=".json") as temp_file:
            temp_file.write('{"hello":"world"}')
            temp_file_path = temp_file.name
        
        save_file(temp_file_path,bucketname,"test_obj",self.url,self.key,self.secret)
        os.remove(temp_file_path)

    def test_getBuckets(self):
        bucketname = str(uuid.uuid4()).replace('-','')
        create_bucket(bucketname,self.url,self.key,self.secret)
        # now search
        buckets = get_buckets(self.url,self.key,self.secret)
        self.assertTrue(len(buckets) > 0)

    def test_listFiles(self):
        #create content
        bucketname = str(uuid.uuid4()).replace('-','')
        with tempfile.NamedTemporaryFile(mode="w+",delete=False,suffix=".json") as temp_file:
            temp_file.write('{"hello":"world"}')
            temp_file_path = temp_file.name
        
        save_file(temp_file_path,bucketname,"test_obj",self.url,self.key,self.secret)
        os.remove(temp_file_path)
        # validate method
        buckets = get_buckets(self.url,self.key,self.secret)
        self.assertTrue(len(buckets) > 0)
        for bucket in buckets:
            files = list_files(bucket,self.url,self.key,self.secret)
            self.assertTrue(len(files) > 0)

    def test_get(self):
        # bucketname = "testbucket"
        bucketname = str(uuid.uuid4()).replace('-','')
        with tempfile.NamedTemporaryFile(mode="w+",delete=False,suffix=".json") as temp_file:
            temp_file.write('{"hello":"world"}')
            temp_file_path = temp_file.name
        
        save_file(temp_file_path,bucketname,"test_obj",self.url,self.key,self.secret)
        os.remove(temp_file_path)
        # create a target temp file
        with tempfile.NamedTemporaryFile(mode="w+",delete=False,suffix=".json") as temp_file:
            pass
        get_file(temp_file_path,bucketname,"test_obj",self.url,self.key,self.secret)
        # now read the file
        with open(temp_file_path,'r') as file:
            content = file.read()
        self.assertTrue(len(content) > 0)
        os.remove(temp_file_path)


    def test_cleanup(self):
        # get all the buckets
        # loop and get all the files
        # delete all the files
        clean_up(self.url,self.key,self.secret)

        
if __name__ == '__main__':
    unittest.main()

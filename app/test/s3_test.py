import unittest
import os
import tempfile
import uuid

from server.service.s3 import get_buckets, list_files, clean_up, create_bucket, create_folder, list_folder_files, save_file_in_folder, get_file_in_folder, get_folders, put_file

class TestS3(unittest.TestCase):

    def setUp(self):
        self.secret = "mytestsecret"
        self.url = "localhost:9000"
        self.key = "mytestkey"


    def tearDown(self):
        clean_up(self.url,self.key,self.secret)

    def test_getBuckets(self):
        bucketname = str(uuid.uuid4()).replace('-','')
        create_bucket(bucketname)
        # now search
        buckets = get_buckets(self.url,self.key,self.secret)
        self.assertTrue(len(buckets) > 0)

    def test_listFiles(self):
        #create content
        bucketname = str(uuid.uuid4()).replace('-','')
        with tempfile.NamedTemporaryFile(mode="w+",delete=False,suffix=".json") as temp_file:
            temp_file.write('{"hello":"world"}')
            temp_file_path = temp_file.name
        
        # save_file(temp_file_path,bucketname,"test_obj",self.url,self.key,self.secret)
        put_file(temp_file_path,"test_obj")
        os.remove(temp_file_path)
        # validate method
        buckets = get_buckets(self.url,self.key,self.secret)
        self.assertTrue(len(buckets) > 0)
        for bucket in buckets:
            # files = list_files(bucket,self.url,self.key,self.secret)
            files = list_files(bucket)
            self.assertTrue(len(files) > 0)

    def test_cleanup(self):
        # get all the buckets
        # loop and get all the files
        # delete all the files
        clean_up(self.url,self.key,self.secret)

    def test_create_folder(self):
        bucketname = str(uuid.uuid4()).replace('-','')
        # create_bucket(bucketname,self.url,self.key,self.secret)
        create_bucket(bucketname)
        # now create the folder
        create_folder(bucketname,"temp_folder",self.url,self.key,self.secret)
        # validate it's there
        files = list_folder_files(bucketname,"temp_folder",self.url,self.key,self.secret)
        self.assertTrue(len(files) == 0) # only the folder should be listed
        # now add some files INSIDE the folder
        with tempfile.NamedTemporaryFile(mode="w+",delete=False,suffix=".json") as temp_file:
            temp_file.write('{"hello":"world"}')
            temp_file_path = temp_file.name
        
        save_file_in_folder(temp_file_path,"temp_folder",bucketname,"test_obj",self.url,self.key,self.secret)
        os.remove(temp_file_path)
        # now list
        files = list_folder_files(bucketname,"temp_folder",self.url,self.key,self.secret)
        self.assertTrue(len(files) == 1) # only the folder should be listed

    def test_get_file_in_folder(self):
        bucketname = str(uuid.uuid4()).replace('-','')
        # create_bucket(bucketname,self.url,self.key,self.secret)
        create_bucket(bucketname)
        # now create the folder
        create_folder(bucketname,"temp_folder",self.url,self.key,self.secret)
        # validate it's there
        files = list_folder_files(bucketname,"temp_folder",self.url,self.key,self.secret)
        self.assertTrue(len(files) == 0) # only the folder should be listed
        # now add some files INSIDE the folder
        with tempfile.NamedTemporaryFile(mode="w+",delete=False,suffix=".json") as temp_file:
            temp_file.write('{"hello":"world"}')
            temp_file_path = temp_file.name
        
        save_file_in_folder(temp_file_path,"temp_folder",bucketname,"test_obj",self.url,self.key,self.secret)
        os.remove(temp_file_path)
        # now list
        files = list_folder_files(bucketname,"temp_folder",self.url,self.key,self.secret)
        self.assertTrue(len(files) == 1) # only a single file
        print(files)
        # retrieve a single file
        with tempfile.NamedTemporaryFile(mode="w+",delete=False,suffix=".json") as temp_file:
            pass
        get_file_in_folder(temp_file_path,"temp_folder",bucketname,"test_obj",self.url,self.key,self.secret)
        # now read the file
        with open(temp_file_path,'r') as file:
            content = file.read()
        self.assertTrue(len(content) > 0)
        os.remove(temp_file_path)
        files = get_folders(bucketname,self.url,self.key,self.secret)
        self.assertTrue(len(files) == 1) # only the folder should be listed        


        
if __name__ == '__main__':
    unittest.main()

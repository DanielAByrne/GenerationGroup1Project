from cgi import test
import pandas.testing # <-- for testing dataframes
import unittest.mock as mock
import pandas as pd
import moto
import pymysql
import hashlib
import logging
import boto3
import os
from moto import mock_s3

# Example from Stack using panda's unittesting library
# class DFTests(unittest.TestCase):
#     """ class for running unittests """

#     def setUp(self):
#         """ Your setUp """
#         #TEST_INPUT_DIR = 'data/'
#         test_file_name =  'testdata.csv'
#         headers=headers
#         try:
#             data = pd.read_csv(test_file_name,headers)
#         except IOError:
#             print('cannot open file')
#         self.fixture = data

#     def test_dataFrame_constructedAsExpected(self):
#         """ Test that the dataframe read in equals what you expect"""
#         foo = pd.DataFrame()
#         assert_frame_equal(self.fixture, foo)


# def execute_query(statement):
#     connection = psycopg2.connect(user=user, password=password, host=host, port=port, database=database)
#     cursor = connection.cursor()
#     cursor.execute(statement)
#     connection.commit()
#     rows = cursor.fetchall()
#     cursor.close()
#     connection.close()
#     return rows

# # @patch
# def test_execute_query(unittest.TestCase):
#     connection = psycopg2.connect(user=user, password=password, host=host, port=port, database=database)
#     cursor = connection.cursor()
#     cursor.execute(statement)
#     connection.commit()
#     rows = cursor.fetchall()
#     cursor.close()
#     connection.close()
#     return rows




# from main import main_etlcl

# LOGGER = logging.getLogger()
# LOGGER.setLevel(logging.INFO)

# def handler(event, context):
#     LOGGER.info(f'Event structure: {event}')
#     bucket = event['Records'][0]['s3']['bucket']['name']
#     key = event['Records'][0]['s3']['object']['key']
#     filename = os.path.basename(key)
#     client = boto3.client('s3')
#     s3 = boto3.resource('s3')
#     s3.meta.client.download_file(bucket, key, f'/tmp/{filename}')

# @mock.patch("")
# def test_handler(event, context):
#     LOGGER.info(f'Event structure: {event}')
#     bucket = event['Records'][0]['s3']['bucket']['name']
#     key = event['Records'][0]['s3']['object']['key']
#     filename = os.path.basename(key)
#     client = boto3.client('s3')
#     s3 = boto3.resource('s3')
#     s3.meta.client.download_file(bucket, key, f'/tmp/{filename}')



#& Tests file download like our lambda
def download_file(filepath,bucket,key):
    s3 = boto3.resource('s3')
    s3.meta.client.download_file(bucket, key, filepath)

@mock_s3()
def test_download_file():
    s3=boto3.client("s3") #fake s3 client
    s3.create_bucket(Bucket="testbucket") #fake s3 bucket
    s3.put_object(Bucket="testbucket",Key="testfile",Body=b"foo-bar") # fake s3 bucket with fake stuff inside
    download_file("testing","testbucket","testfile") #insert our args from the func "download_file(filepath,bucket,key)
    assert os.path.isfile("testing")#< the fake file called test
# so all above commands are "fake", an asserting is "real"


#real func df pd:
# def create_dataframe(filepath,columns):
#     df = pd.read_csv(filepath, header=None)
#     df.columns = columns
#     return df
#! must have above function in different file,then import to here for test below to work
#*mock unittest func using df pd:
from functest import create_dataframe 
@mock.patch("functest.pd.read_csv") #filename which we're patching - must be a string
def test_create_dataframe(read_csv_mock:mock.Mock):
    read_csv_mock.return_value=pd.DataFrame({"foo_id": [1, 2, 3]}) #can be anything , see below notes
    results=create_dataframe("test.csv",["bar_id"]) #mock csv, then change column name, then renaming it, bar had ot be in a list because columns
    read_csv_mock.assert_called_once()
    pd.testing.assert_frame_equal(results, pd.DataFrame({"bar_id": [1, 2, 3]}))


#^ = made a new file so we cant mock test patch the entire file as pd
#* Next steps: when mocking other func,, do dummy chesterfield with 2 rows/columns


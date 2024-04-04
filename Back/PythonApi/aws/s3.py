import boto3
from aws.env import *

s3_client = boto3.client("s3", aws_access_key_id=AWS_ACCESS_S3,aws_secret_access_key=AWS_SECRET_S3)

def putobject(key, file_contents):
    s3_client.put_object(Bucket=BUCKET_NAME, Key=key, Body=file_contents)
    
def s3_getlink(key):
    link = s3_client.generate_presigned_url('get_object', Params={'Bucket':BUCKET_NAME, 'Key':key, }, ExpiresIn=None);
    return link


    
def deleteobject(key, file_contents):
    s3_client.put_object(Bucket=BUCKET_NAME, Key=key, Body=file_contents)
    link = s3_client.generate_presigned_url('get_object', Params={'Bucket':BUCKET_NAME, 'Key':key, }, ExpiresIn=None);
    return link


    
def getobject(key, file_contents):
    s3_client.put_object(Bucket=BUCKET_NAME, Key=key, Body=file_contents)
    link = s3_client.generate_presigned_url('get_object', Params={'Bucket':BUCKET_NAME, 'Key':key, }, ExpiresIn=None);
    return link


    
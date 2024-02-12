import boto3
from pathlib import Path
import os
import json
from .ObjectStorage import ObjectStorage

class S3(ObjectStorage):
    def __init__(self):
        configs_file_path = os.path.join(Path(__file__).parent.absolute(), 'secret', 'configs.json')
        with open(configs_file_path) as f:
            configs = json.load(f)
            self.s3 = boto3.client(
                service_name='s3',
                region_name=configs["REGION"], 
                aws_access_key_id=configs["ACCESS_KEY"],
                aws_secret_access_key=configs["SECRET_ACCESS_KEY"]
            )
            self.bucket = configs['BUCKET_NAME']

    def delete(self, object_id):
        try:
            response = self.s3.delete_object(
                Bucket=self.bucket,
                Key=object_id,
            )
            return response['DeleteMarket']
        except:
            return False
    
    def isExist(self, object_id):
        try:
            self.s3.head_object(Bucket=self.bucket, Key=object_id)
            return True
        except:
            return False
        
    def save(self, file, access_key, content_type):
        try:
            self.s3.put_object(
                Body=file,
                Bucket=self.bucket,
                Key=access_key,
                ContentType=content_type,
            )
        except Exception as e:
            print(e)


        

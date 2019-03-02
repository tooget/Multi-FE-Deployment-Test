from troposphere import Template
from troposphere.s3 import Bucket, Private


class S3Privates(object):
    def __init__(self, sceptre_user_data):
        self.template = Template()
        self.sceptreUserData = sceptre_user_data
        self._createS3Bucket()
    
    def _createS3Bucket(self):
        self.s3 = self.template.add_resource(Bucket(
            self.sceptreUserData['s3_bucket'],
            BucketName = self.sceptreUserData['s3_hosting_subdomain_url'],
            AccessControl = Private
        ))

def sceptre_handler(sceptre_user_data):
    s3private = S3Privates(sceptre_user_data)
    print(s3private.template.to_yaml())
    return s3private.template.to_yaml()
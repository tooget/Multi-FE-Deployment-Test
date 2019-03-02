from troposphere import Template, Ref, Join
from troposphere.s3 import Bucket, BucketPolicy, WebsiteConfiguration


class S3Publics(object):
    def __init__(self, sceptre_user_data):
        self.template = Template()
        self.sceptreUserData = sceptre_user_data
        self._createS3Bucket()
        self._addPolicyToS3Bucket()
    
    def _createS3Bucket(self):
        self.s3 = self.template.add_resource(Bucket(
                self.sceptreUserData['s3_bucket'],
                BucketName = self.sceptreUserData['s3_hosting_subdomain_url'],
                WebsiteConfiguration = WebsiteConfiguration(
                    IndexDocument = self.sceptreUserData['s3_hosting_rootfile'],
                    ErrorDocument = self.sceptreUserData['s3_hosting_rootfile'],
                )))
    
    def _addPolicyToS3Bucket(self):
        self.s3Policy = self.template.add_resource(BucketPolicy(
            self.sceptreUserData['s3_policy'],
            Bucket = Ref(self.s3),
            PolicyDocument = {
                "Version": "2012-10-17",
                "Statement": [{
                    "Effect": "Allow",
                    "Principal": "*",
                    "Action": ["s3:GetObject"],
                    "Resource": [Join("", ["arn:aws:s3:::", Ref(self.s3) , "/*" ])]
                }]
            }
        ))

def sceptre_handler(sceptre_user_data):
    s3public = S3Publics(sceptre_user_data)
    print(s3public.template.to_yaml())
    return s3public.template.to_yaml()
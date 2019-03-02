from troposphere import Template, Parameter, Output, Ref, Tags
from troposphere.ec2 import VPC


class Vpcs(object):
    def __init__(self, sceptre_user_data):
        self.template = Template()
        self.sceptreUserData = sceptre_user_data
        self._createVpc()
        self._addVpcIdOutput()

    def _createVpc(self):
        self.vpc = self.template.add_resource(VPC(
            self.sceptreUserData['vpc_prefix'],
            CidrBlock = self.sceptreUserData['vpc_params_cidrblock'],
            EnableDnsSupport = True,
            EnableDnsHostnames = True,
            Tags = Tags(
                Name = Ref("AWS::StackName"),
            )
        ))
    
    def _addVpcIdOutput(self):
        self.template.add_output(Output(
            self.sceptreUserData['vpc_params_vpcid_prefix'],
            Value = Ref(self.vpc),
        ))

def sceptre_handler(sceptre_user_data):
    vpc = Vpcs(sceptre_user_data)
    # print(vpc.template.to_yaml())
    return vpc.template.to_yaml()
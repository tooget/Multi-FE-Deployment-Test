from troposphere import Template, Ref, Tags, Join
from troposphere.ec2 import Subnet


class Subnets(object):
    def __init__(self, sceptre_user_data):
        self.template = Template()
        self.sceptreUserData = sceptre_user_data
        self._createSubnet(
            self.sceptreUserData['subnet_prefix'],
            self.sceptreUserData['subnet_vpcid'],
            self.sceptreUserData['subnet_params_cidrblock'],
            self.sceptreUserData['subnet_params_azlocation'],
            self.sceptreUserData['subnet_params_access'],
        )

    def _createSubnet(self, subnet_prefix, vpcid, cidr_params, az_params, access_params):
        self.subnet = self.template.add_resource(Subnet(
            subnet_prefix,
            VpcId = vpcid,
            CidrBlock = cidr_params,
            AvailabilityZone = az_params,
            Tags = Tags(
                Name = Join('',[Ref('AWS::StackName'), access_params]),
            )
        ))

def sceptre_handler(sceptre_user_data):
    subnet = Subnets(sceptre_user_data)
    print(subnet.template.to_yaml())
    return subnet.template.to_yaml()
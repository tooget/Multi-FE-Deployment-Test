from troposphere import Template, Output, Ref, Tags
from troposphere.ec2 import InternetGateway, VPCGatewayAttachment


class InternetGateways(object):
    def __init__(self, sceptre_user_data):
        self.template = Template()
        self.sceptreUserData = sceptre_user_data
        self._createIgw()
        self._attachIgwToVpc()
        self._addIgwIdOutput()

    def _createIgw(self):
        self.igw = self.template.add_resource(InternetGateway(
            self.sceptreUserData['igw_prefix'],
            Tags = Tags(
                Name = Ref("AWS::StackName"),
            )
        ))

    def _attachIgwToVpc(self):
        self.template.add_resource(VPCGatewayAttachment(
            self.sceptreUserData['igw_params_attachment_prefix'],
            VpcId = self.sceptreUserData['igw_vpcid'],
            InternetGatewayId = Ref(self.igw),
        ))

    def _addIgwIdOutput(self):
        self.template.add_output(Output(
            self.sceptreUserData['igw_params_igwid_prefix'],
            Value = Ref(self.igw),
        ))

def sceptre_handler(sceptre_user_data):
    igw = InternetGateways(sceptre_user_data)
    # print(igw.template.to_yaml())
    return igw.template.to_yaml()
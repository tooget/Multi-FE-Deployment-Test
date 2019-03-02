from troposphere import Template, Output, Ref, Tags
from troposphere.ec2 import InternetGateway, VPCGatewayAttachment, Route


class InternetGateways(object):
    def __init__(self, sceptre_user_data):
        self.template = Template()
        self.sceptreUserData = sceptre_user_data
        self._createIgw()
        self._attachIgwToVpc()
        self._attachRtbToIgw(
            self.sceptreUserData['igw_params_publicrtb_prefix'],
            self.sceptreUserData['igw_params_publicrtb_rtbid'],
            self.sceptreUserData['igw_params_rtbdestination_cidrblock'],
        )
        self._attachRtbToIgw(
            self.sceptreUserData['igw_params_privatertb_prefix'],
            self.sceptreUserData['igw_params_privatertb_rtbid'],
            self.sceptreUserData['igw_params_rtbdestination_cidrblock'],
        )

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

    def _attachRtbToIgw(self, rtb_prefix, rtbid, destination_cidrblock):
        self.template.add_resource(Route(
            rtb_prefix,
            GatewayId = Ref(self.igw),
            RouteTableId = rtbid,
            DestinationCidrBlock = destination_cidrblock
        ))

    def _addIgwIdOutput(self):
        self.template.add_output(Output(
            self.sceptreUserData['vpc_params_vpcid_prefix'],
            Value = Ref(self.vpc),
        ))

def sceptre_handler(sceptre_user_data):
    igw = InternetGateways(sceptre_user_data)
    # print(igw.template.to_yaml())
    return igw.template.to_yaml()
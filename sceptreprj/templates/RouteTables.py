from troposphere import Template, Output, Ref, Tags, Join
from troposphere.ec2 import RouteTable, SubnetRouteTableAssociation


class RouteTables(object):
    def __init__(self, sceptre_user_data):
        self.template = Template()
        self.sceptreUserData = sceptre_user_data
        self.publicRtb = self._createRtb(
            self.sceptreUserData['rtb_params_public_prefix'],
            self.sceptreUserData['rtb_vpcid'],
            self.sceptreUserData['rtb_params_public_access'],
        )
        self.privateRtb = self._createRtb(
            self.sceptreUserData['rtb_params_private_prefix'],
            self.sceptreUserData['rtb_vpcid'],
            self.sceptreUserData['rtb_params_private_access'],
        )
        self._associateRtbToSubnet(
            self.sceptreUserData['rtb_params_associate_publicsubnet1_prefix'],
            self.sceptreUserData['rtb_params_associate_publicsubnet1_subnetid'],
            Ref(self.publicRtb),
        )
        self._associateRtbToSubnet(
            self.sceptreUserData['rtb_params_associate_privatesubnet1_prefix'],
            self.sceptreUserData['rtb_params_associate_privatesubnet1_subnetid'],
            Ref(self.privateRtb),
        )
        self._associateRtbToSubnet(
            self.sceptreUserData['rtb_params_associate_privatesubnet2_prefix'],
            self.sceptreUserData['rtb_params_associate_privatesubnet2_subnetid'],
            Ref(self.privateRtb),
        )
        self._addSubnetIdOutput()

    def _createRtb(self, rtb_params_prefix, vpcid, rtb_params_access):
        rtb = self.template.add_resource(RouteTable(
            rtb_params_prefix,
            VpcId = vpcid,
            Tags = Tags(
                Name = Join('', [Ref('AWS::StackName'), rtb_params_access]),
            )
        ))
        return rtb
    
    def _associateRtbToSubnet(self, associate_prefix, subnetid, rtbid):
        self.template.add_resource(SubnetRouteTableAssociation(
            associate_prefix,
            SubnetId = subnetid,
            RouteTableId = rtbid,
        ))
    
    def _addSubnetIdOutput(self):
        self.template.add_output([
            Output(
                self.sceptreUserData['rtb_params_publicrtbid_prefix'],
                Value = Ref(self.publicRtb),
            ),
            Output(
                self.sceptreUserData['rtb_params_privatertbid_prefix'],
                Value = Ref(self.privateRtb),
            )
        ])

def sceptre_handler(sceptre_user_data):
    rtb = RouteTables(sceptre_user_data)
    # print(rtb.template.to_yaml())
    return rtb.template.to_yaml()
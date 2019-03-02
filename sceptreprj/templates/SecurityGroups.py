from troposphere import Template, Output, Ref
from troposphere.ec2 import SecurityGroup, SecurityGroupRule


class SecurityGroups(object):
    def __init__(self, sceptre_user_data):
        self.template = Template()
        self.sceptreUserData = sceptre_user_data
        self._createSg()
        self._addSgIdOutput()

    def _createSg(self):
        self.sg = self.template.add_resource(SecurityGroup(
            self.sceptreUserData['sg_prefix'],
            GroupDescription = self.sceptreUserData['sg_params_description'],
            SecurityGroupIngress = [
                SecurityGroupRule(
                    IpProtocol = self.sceptreUserData['sg_params_ingress1_prefix'],
                    FromPort = self.sceptreUserData['sg_params_ingress1_fromport'],
                    ToPort = self.sceptreUserData['sg_params_ingress1_toport'],
                    CidrIp = self.sceptreUserData['sg_params_ingress1_cidrip'],
                ),
                SecurityGroupRule(
                    IpProtocol = self.sceptreUserData['sg_params_ingress2_prefix'],
                    FromPort = self.sceptreUserData['sg_params_ingress2_fromport'],
                    ToPort = self.sceptreUserData['sg_params_ingress2_toport'],
                    CidrIp = self.sceptreUserData['sg_params_ingress2_cidrip'],
                ),
                SecurityGroupRule(
                    IpProtocol = self.sceptreUserData['sg_params_ingress3_prefix'],
                    FromPort = self.sceptreUserData['sg_params_ingress3_fromport'],
                    ToPort = self.sceptreUserData['sg_params_ingress3_toport'],
                    CidrIp = self.sceptreUserData['sg_params_ingress3_cidrip'],
                ),
                SecurityGroupRule(
                    IpProtocol = self.sceptreUserData['sg_params_ingress4_prefix'],
                    FromPort = self.sceptreUserData['sg_params_ingress4_fromport'],
                    ToPort = self.sceptreUserData['sg_params_ingress4_toport'],
                    CidrIp = self.sceptreUserData['sg_params_ingress4_cidrip'],
                ),
                SecurityGroupRule(
                    IpProtocol = self.sceptreUserData['sg_params_ingress5_prefix'],
                    FromPort = self.sceptreUserData['sg_params_ingress5_fromport'],
                    ToPort = self.sceptreUserData['sg_params_ingress5_toport'],
                    CidrIp = self.sceptreUserData['sg_params_ingress5_cidrip'],
                ),
            ],
            VpcId = self.sceptreUserData['sg_vpcid'],
        ))
    
    def _addSgIdOutput(self):
        self.template.add_output(Output(
            self.sceptreUserData['sg_params_sgid_prefix'],
            Value = Ref(self.sg),
        ))

def sceptre_handler(sceptre_user_data):
    sg = SecurityGroups(sceptre_user_data)
    # print(sg.template.to_yaml())
    return sg.template.to_yaml()

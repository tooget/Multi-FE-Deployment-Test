from troposphere import Template, Output, Ref, Tags
from troposphere.ec2 import Route


class IgwRtbRoutings(object):
    def __init__(self, sceptre_user_data):
        self.template = Template()
        self.sceptreUserData = sceptre_user_data
        self._attachRtbToIgw(
            self.sceptreUserData['igwrtbattachment_params_igwid'],
            self.sceptreUserData['igwrtbattachment_params_publicrtb_prefix'],
            self.sceptreUserData['igwrtbattachment_params_publicrtb_rtbid'],
            self.sceptreUserData['igwrtbattachment_params_rtbdestination_cidrblock'],
        )
        self._attachRtbToIgw(
            self.sceptreUserData['igwrtbattachment_params_igwid'],
            self.sceptreUserData['igwrtbattachment_params_privatertb_prefix'],
            self.sceptreUserData['igwrtbattachment_params_privatertb_rtbid'],
            self.sceptreUserData['igwrtbattachment_params_rtbdestination_cidrblock'],
        )

    def _attachRtbToIgw(self, igwid, rtb_prefix, rtbid, destination_cidrblock):
        self.template.add_resource(Route(
            rtb_prefix,
            GatewayId = igwid,
            RouteTableId = rtbid,
            DestinationCidrBlock = destination_cidrblock
        ))

def sceptre_handler(sceptre_user_data):
    igwrtb = IgwRtbRoutings(sceptre_user_data)
    # print(igwrtb.template.to_yaml())
    return igwrtb.template.to_yaml()
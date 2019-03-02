from troposphere import Template, Parameter, Output, Ref, Tags
from troposphere.rds import DBSubnetGroup


class DBSubnetGroups(object):
    def __init__(self, sceptre_user_data):
        self.template = Template()
        self.sceptreUserData = sceptre_user_data
        self._createDBSg()
        self._addDBSgIdOutput()

    def _createDBSg(self):
        self.dbsg = self.template.add_resource(DBSubnetGroup(
            self.sceptreUserData['dbsg_prefix'],
            DBSubnetGroupDescription = self.sceptreUserData['dbsg_params_description'],
            SubnetIds = [
                self.sceptreUserData['dbsg_params_privatesubnet1_subnetid'],
                self.sceptreUserData['dbsg_params_privatesubnet2_subnetid'],
            ]
        ))
    
    def _addDBSgIdOutput(self):
        self.template.add_output(Output(
            self.sceptreUserData['dbsg_params_dbsgid_prefix'],
            Value = Ref(self.dbsg),
        ))

def sceptre_handler(sceptre_user_data):
    dbsg = DBSubnetGroups(sceptre_user_data)
    # print(dbsg.template.to_yaml())
    return dbsg.template.to_yaml()
from troposphere import Template, Parameter, Output, GetAtt
from troposphere.rds import DBCluster, ScalingConfiguration


class DBClusters(object):
    def __init__(self, sceptre_user_data):
        self.template = Template()
        self.sceptreUserData = sceptre_user_data
        self._createDBCluster()
        self._addDBClusterIdOutput()

    def _createDBCluster(self):
        self.dbcluster = self.template.add_resource(DBCluster(
            self.sceptreUserData['dbcluster_prefix'],
            Engine = self.sceptreUserData['dbcluster_params_dbengine_prefix'],
            EngineVersion = self.sceptreUserData['dbcluster_params_dbengine_version'],
            EngineMode = self.sceptreUserData['dbcluster_params_dbengine_mode'],
            ScalingConfiguration = ScalingConfiguration(
                MinCapacity = self.sceptreUserData['dbcluster_params_scaling_mincapacity'],
                MaxCapacity = self.sceptreUserData['dbcluster_params_scaling_maxcapacity'],
                SecondsUntilAutoPause = self.sceptreUserData['dbcluster_params_scaling_autopausesec']    # Only for Aurora-Serverless, seconds
            ),
            DBSubnetGroupName = self.sceptreUserData['dbcluster_params_dbsg_dbsgid'],
            VpcSecurityGroupIds = [
                self.sceptreUserData['dbcluster_params_sg_sgid'],
            ],
            DBClusterIdentifier = self.sceptreUserData['dbcluster_params_identifier'],
            MasterUsername = self.sceptreUserData['dbcluster_params_master_username'],
            MasterUserPassword = self.sceptreUserData['dbcluster_params_master_userpassword'],
        ))
    
    def _addDBClusterIdOutput(self):
        self.template.add_output([
            Output(
                self.sceptreUserData['dbcluster_params_dbendpoint_prefix'],
                Value = GetAtt(self.dbcluster, self.sceptreUserData['dbcluster_params_dbendpoint_getatt']),
            ),
            Output(
                self.sceptreUserData['dbcluster_params_master_username_prefix'],
                Value = self.sceptreUserData['dbcluster_params_master_username'],
            ),
            Output(
                self.sceptreUserData['dbcluster_params_master_userpassword_prefix'],
                Value = self.sceptreUserData['dbcluster_params_master_userpassword'],
            ),
        ])

def sceptre_handler(sceptre_user_data):
    dbcluster = DBClusters(sceptre_user_data)
    # print(dbcluster.template.to_yaml())
    return dbcluster.template.to_yaml()

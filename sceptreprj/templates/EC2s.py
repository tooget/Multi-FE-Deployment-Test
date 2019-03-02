from troposphere import Template, Parameter, Output, Ref, Tags, Base64, Join, Sub
from troposphere.ec2 import Instance, NetworkInterfaceProperty


class EC2s(object):
    def __init__(self, sceptre_user_data):
        self.template = Template()
        self.sceptreUserData = sceptre_user_data
        self.mysqlCommandSubMapper = {
            'dbhost': self.sceptreUserData['ec2_params_userdata_dbhost'],
            'dbusername': self.sceptreUserData['ec2_params_userdata_dbusername'],
            'dbuserpassword': self.sceptreUserData['ec2_params_userdata_dbuserpassword'],
        }
        self._createEC2()

    def _createEC2(self):
        self.ec2 = self.template.add_resource(Instance(
            self.sceptreUserData['ec2_prefix'],
            ImageId = self.sceptreUserData['ec2_params_instance_imageid'],
            InstanceType = self.sceptreUserData['ec2_params_instance_type'],
            KeyName = self.sceptreUserData['ec2_params_instance_keyname'],
            NetworkInterfaces = [NetworkInterfaceProperty(
                GroupSet = [
                    self.sceptreUserData['ec2_params_instance_sg_sgid'],
                ],
                AssociatePublicIpAddress = self.sceptreUserData['ec2_params_instance_publicip_access'],
                DeviceIndex = self.sceptreUserData['ec2_params_instance_deviceindex'],
                DeleteOnTermination = self.sceptreUserData['ec2_params_instance_deleteontermination'],
                SubnetId = self.sceptreUserData['ec2_params_instance_publicsubnet1_subnetid'],
            )],
            UserData = Base64(Join("\n", [
                "#!/bin/bash",
                "sudo apt-get update && sudo apt-get -y install mysql-client awscli",
                Sub("mysql --protocol=tcp --host=${dbhost} --port=3306 --user=${dbusername} --password=${dbuserpassword} --execute='CREATE SCHEMA `simplesmartcheck` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_520_ci;'", **self.mysqlCommandSubMapper),
                Sub("mysql --protocol=tcp --host=${dbhost} --port=3306 --user=${dbusername} --password=${dbuserpassword} --execute='CREATE SCHEMA `simplesmartcheckusers` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_520_ci;'", **self.mysqlCommandSubMapper)
            ])),
        ))
        print("mysql --protocol=tcp --host=${dbhost} --port=3306 --user=${dbusername} --password=${dbuserpassword}".format(**self.mysqlCommandSubMapper))

def sceptre_handler(sceptre_user_data):
    ec2 = EC2s(sceptre_user_data)
    # print(ec2.template.to_yaml())
    return ec2.template.to_yaml()

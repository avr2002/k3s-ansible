# /// script
# requires-python = ">=3.8"
# dependencies = ["aws-cdk-lib", "constructs"]
# ///

# To use this infrastructure:
# 1. Deploy: cdk deploy
# 2. Download private key: aws ssm get-parameter --name "/ec2/keypair/cluster-keypair" --with-decryption --query "Parameter.Value" --output text > cluster-key.pem
# 3. Set permissions: chmod 400 cluster-key.pem
# 4. SSH to instance: ssh -i cluster-key.pem ec2-user@<PUBLIC_IP>

import os
from pathlib import Path
from aws_cdk import App, Stack, Environment, CfnOutput
from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_iam as iam
from constructs import Construct

THIS_DIR = Path(__file__).parent

VPC_NAME = "local-oregon"


class K8sClusterStack(Stack):
    def __init__(
        self, scope: Construct, construct_id: str, instance_count: int = 3, **kwargs
    ):
        super().__init__(scope, construct_id, **kwargs)

        # vpc = ec2.Vpc.from_lookup(self, "DefaultVpc", is_default=True)
        if VPC_NAME.lower() == "default":
            vpc = ec2.Vpc.from_lookup(self, "VpcLookup", is_default=True)
        else:
            vpc = ec2.Vpc.from_lookup(
                self,
                "VpcLookup",
                vpc_name=VPC_NAME,
            )
        security_group = create_security_group(self, vpc)

        # Create IAM role for EC2 instances
        # instance_role = create_instance_role(self)

        key_pair = ec2.KeyPair(self, "ClusterKeyPair", key_pair_name="cluster-keypair")

        instances = []
        for i in range(instance_count):
            instance = ec2.Instance(
                self,
                f"Instance{i}",
                instance_type=ec2.InstanceType.of(
                    ec2.InstanceClass.T3, ec2.InstanceSize.MEDIUM
                ),
                machine_image=ec2.MachineImage.latest_amazon_linux2023(),
                # machine_image=ec2.MachineImage.from_ssm_parameter(
                #     "/aws/service/canonical/ubuntu/server/22.04/stable/current/amd64/hvm/ebs-gp2/ami-id"
                # ),
                vpc=vpc,
                security_group=security_group,
                key_pair=key_pair,
                vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
                # role=instance_role,
                # user_data=ec2.UserData.for_linux(),
            )

            # # Configure AWS CLI with region
            # instance.user_data.add_commands(
            #     "#!/bin/bash",
            #     "yum update -y",
            #     f"aws configure set region {self.region}",
            #     "echo 'export AWS_DEFAULT_REGION={region}' >> /etc/environment".format(
            #         region=self.region
            #     ),
            #     "echo 'AWS CLI configured with region: {region}' > /home/ec2-user/aws-config-status.txt".format(
            #         region=self.region
            #     ),
            # )

            instances.append(instance)

            # Create individual output for each instance
            CfnOutput(
                self,
                f"Instance{i}PublicIP",
                value=instance.instance_public_ip,
                description=f"Public IP of Instance {i}",
            )

        CfnOutput(self, "KeyPairName", value=key_pair.key_pair_name)
        CfnOutput(self, "KeyPairId", value=key_pair.key_pair_id)


def create_security_group(scope: Construct, vpc: ec2.Vpc) -> ec2.SecurityGroup:
    sg = ec2.SecurityGroup(scope, "InstanceSecurityGroup", vpc=vpc)
    sg.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(22))
    sg.add_ingress_rule(sg, ec2.Port.all_traffic())

    # kubectl
    sg.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(6443))

    return sg


def create_instance_role(scope: Construct) -> iam.Role:
    """Create IAM role for EC2 instances with EC2 describe permissions"""

    # Create IAM role that EC2 can assume
    role = iam.Role(
        scope,
        "InstanceRole",
        assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"),
        description="IAM role for K3s cluster EC2 instances",
        # This automatically creates an instance profile with the same name as the role
        role_name="K3sClusterInstanceRole",
    )

    # Add EC2 describe permissions
    role.add_to_policy(
        iam.PolicyStatement(
            effect=iam.Effect.ALLOW,
            actions=[
                "ec2:DescribeInstances",
                "ec2:DescribeInstanceTypes",
                "ec2:DescribeRegions",
                "ec2:DescribeAvailabilityZones",
                "ec2:DescribeSubnets",
                "ec2:DescribeVpcs",
                "ec2:DescribeNetworkInterfaces",
            ],
            resources=["*"],
        )
    )

    return role


app = App()
K8sClusterStack(
    app,
    "cluster",
    env=Environment(
        account=os.environ.get("CDK_DEFAULT_ACCOUNT"),
        region=os.environ.get("CDK_DEFAULT_REGION"),
    ),
    instance_count=3,
)
app.synth()

import pathlib

from aws_cdk import Stack, aws_ec2, aws_lambda
from constructs import Construct

VPC_CIDR = "10.11.0.0/16"
PRIVATE_SUBNET_1_CIDR = "10.11.10.0/24"
PRIVATE_SUBNET_2_CIDR = "10.11.20.0/24"

SUBNETS_NAME = "HogePrivate"


class CdkNetworkStack1(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # VPC
        vpc = aws_ec2.Vpc(
            self,
            "vpc1",
            cidr=VPC_CIDR,
            max_azs=2,
            subnet_configuration=[
                aws_ec2.SubnetConfiguration(
                    name=SUBNETS_NAME,
                    cidr_mask=24,
                    subnet_type=aws_ec2.SubnetType.PRIVATE_ISOLATED,
                )
            ],
        )
        # SubnetのCidrBlockを上書きする
        selection = vpc.select_subnets(
            subnet_group_name=SUBNETS_NAME,
        )
        for cider, subnet in zip(
            [PRIVATE_SUBNET_1_CIDR, PRIVATE_SUBNET_2_CIDR], selection.subnets
        ):
            cfn_subnet: aws_ec2.CfnSubnet = subnet.node.default_child
            cfn_subnet.cidr_block = cider

        # （おまけ）VPCにLambdaを乗せる場合の設定例

        aws_lambda.Function(
            self,
            "function1",
            code=aws_lambda.Code.from_asset(
                str(pathlib.Path(__file__).resolve().parent.joinpath("runtime"))
            ),
            runtime=aws_lambda.Runtime.PYTHON_3_9,
            handler="index.handler",
            vpc=vpc,
            vpc_subnets=aws_ec2.SubnetSelection(
                subnet_type=aws_ec2.SubnetType.PRIVATE_ISOLATED
            ),
            security_groups=[aws_ec2.SecurityGroup(self, "SG1", vpc=vpc)],
        )

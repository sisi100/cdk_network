import pathlib

from aws_cdk import Stack, aws_ec2, aws_lambda
from constructs import Construct

VPC_CIDR = "10.22.0.0/16"
PRIVATE_SUBNET_1_CIDR = "10.22.10.0/24"
PRIVATE_SUBNET_2_CIDR = "10.22.20.0/24"
PRIVATE_SUBNET_1_AVAILABILITY_ZONE = "ap-northeast-1a"
PRIVATE_SUBNET_2_AVAILABILITY_ZONE = "ap-northeast-1c"


class CdkNetworkStack2(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # VPC
        vpc = aws_ec2.Vpc(
            self,
            "vpc2",
            cidr=VPC_CIDR,
            subnet_configuration=[],  # 明示的に空にしないとSubnetが自動で作られる
        )

        # Subnet
        vpc_subnets = [
            aws_ec2.Subnet(
                self,
                "Private1",
                availability_zone=PRIVATE_SUBNET_1_AVAILABILITY_ZONE,
                cidr_block=PRIVATE_SUBNET_1_CIDR,
                vpc_id=vpc.vpc_id,
            ),
            aws_ec2.Subnet(
                self,
                "Private2",
                availability_zone=PRIVATE_SUBNET_2_AVAILABILITY_ZONE,
                cidr_block=PRIVATE_SUBNET_2_CIDR,
                vpc_id=vpc.vpc_id,
            ),
        ]

        # （おまけ）VPCにLambdaを乗せる場合の設定例

        aws_lambda.Function(
            self,
            "function2",
            code=aws_lambda.Code.from_asset(
                str(pathlib.Path(__file__).resolve().parent.joinpath("runtime"))
            ),
            runtime=aws_lambda.Runtime.PYTHON_3_9,
            handler="index.handler",
            vpc=vpc,
            vpc_subnets=aws_ec2.SubnetSelection(
                subnets=vpc_subnets,
            ),
            security_groups=[aws_ec2.SecurityGroup(self, "SG2", vpc=vpc)],
        )

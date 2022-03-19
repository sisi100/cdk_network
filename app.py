#!/usr/bin/env python3
import os

import aws_cdk as cdk

from cdk_network.cdk_network_stack_1 import CdkNetworkStack1
from cdk_network.cdk_network_stack_2 import CdkNetworkStack2

app = cdk.App()
CdkNetworkStack1(app, "CdkNetworkStack1")
CdkNetworkStack2(app, "CdkNetworkStack2")

app.synth()

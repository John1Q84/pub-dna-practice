from aws_cdk import(
    aws_ec2 as ec2,
    core
)


class CdkEc2SecurityGroup(core.Stack):
    def __init__(self, scope: core.Construct, id: str, vpc, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self.myAlbSecurityGroup=ec2.SecurityGroup(
            self, "pubAlbSg", 
            vpc=vpc,
            description="public alb security group",
            security_group_name="pubAlbSg",
            allow_all_outbound=False
        )
        self.myAlbSecurityGroup.add_ingress_rule(
            ec2.Peer.any_ipv4(), 
            ec2.Port.tcp(80),
            description="allow public http access",
        )    
        self.myEcsSecurityGroup=ec2.SecurityGroup(
            self, "intMyEcsAppSg",
            vpc=vpc,
            description="allow traffic from internal alb",
            security_group_name="intlEcsAppSg",
            allow_all_outbound=True
        )
        self.myEcsSecurityGroup.connections.allow_from(
            self.myAlbSecurityGroup.connections, 
            ec2.Port.all_tcp(),
            description="allow access from the alb"
        )
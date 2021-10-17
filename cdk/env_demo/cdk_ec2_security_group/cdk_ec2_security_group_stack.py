from aws_cdk import(
    aws_ec2 as ec2,
    core
)


class CdkEc2SecurityGroup(core.Stack):
    def __init__(self, scope: core.Construct, id: str, vpc, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        
        ## public alb security group
        self.myPubAlbSecurityGroup=ec2.SecurityGroup(
            self, "pubAlbSg", 
            vpc=vpc,
            description="public alb security group",
            security_group_name="pubAlbSg",
            allow_all_outbound=False
        )
        self.myPubAlbSecurityGroup.add_ingress_rule(
            ec2.Peer.any_ipv4(), 
            ec2.Port.tcp(80),
            description="allow public http access",
        )    

        ## private alb security group
        self.myPrivAlbSecurityGroup=ec2.SecurityGroup(
            self, "privAlbSg", 
            vpc=vpc,
            description="private alb security group",
            security_group_name="privAlbSg",
            allow_all_outbound=False
        )
        self.myPrivAlbSecurityGroup.add_ingress_rule(
            ec2.Peer.ipv4("10.10.0.0/16"), 
            ec2.Port.tcp(80),
            description="allow http access from VPC cidr ranage",
        )
        
        ## vpc ecs security group
        self.myEcsSecurityGroup=ec2.SecurityGroup(
            self, "intMyEcsAppSg",
            vpc=vpc,
            description="allow traffic from Albs",
            security_group_name="intlEcsAppSg",
            allow_all_outbound=True
        )
        self.myEcsSecurityGroup.connections.allow_from(
            self.myPubAlbSecurityGroup.connections, 
            ec2.Port.all_tcp(),
            description="allow access from the PubAlb"
        )
        self.myEcsSecurityGroup.connections.allow_from(
            self.myPrivAlbSecurityGroup.connections, 
            ec2.Port.all_tcp(),
            description="allow access from the PrivAlb"
        )
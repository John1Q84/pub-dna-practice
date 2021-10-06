from aws_cdk import (
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_ecr as ecr,
    aws_elasticloadbalancingv2 as elb,
    aws_ecs_patterns as ecs_patterns,
    core
)

class CdkEcsFgtCluster(core.Stack):
    def __init__(self, scope: core.Construct, id: str, vpc, **kwargs) -> None :
        super().__init__(scope, id, **kwargs)

        # Cluster
        self.myCluster=ecs.Cluster(
            self, "ecsCluster",
            vpc=vpc,
            capacity_providers=['FARGATE'],
            container_insights=True,
            cluster_name=id
        )

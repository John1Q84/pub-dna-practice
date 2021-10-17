#!/usr/bin/env python3

from aws_cdk import core
from cdk_vpc.cdk_vpc_stack import CdkVpcStack as vpc
from cdk_ecs_fargate.cdk_ecs_fargate_stack import CdkEcsFgtStack as ecs
from cdk_ec2_security_group.cdk_ec2_security_group_stack import CdkEc2SecurityGroup as sg
from cdk_ecs_cluster.cdk_ecs_cluster_stack import CdkEcsFgtCluster as cluster
    


app=core.App()

vpc_stack=vpc(app, "myAwsomeVpc")
## Create, alb security-group and ecs security-group
## each can be referred by sg.myEcsSecurityGroup and sg.myAlbSecurityGroup
# The alb SG allows traffic from internet http port, the ecs SG allow traffic from the alb SG
sgStack=sg(app, "mySgSet1", vpc=vpc_stack.vpc) 

## Create ECS Fargate cluster, attribute id should be the cluster name
ecsFgtClusterStack=cluster(app, "myEcsCluster", vpc=vpc_stack.vpc)
                    
blueEcsFgtServiceStack=ecs(
    app, "myAwsomeEcsBlue", 
    vpc=vpc_stack.vpc,
    tag="blue",
    alb_sg=sgStack.myAlbSecurityGroup,
    ecs_sg=sgStack.myEcsSecurityGroup,
    cluster=ecsFgtClusterStack.myCluster,
    # repo_arn = "arn:aws:ecr:ap-northeast-2:499656329194:repository/ym_demo_ecr", 
    ## public repo uri : public.ecr.aws/n3g9h1h6/ym-ecr/abp:latest
    image_uri="public.ecr.aws/n3g9h1h6/ym-ecr/abp:blue"
    
)

greenEcsFgtServiceStack=ecs(
    app, "myAwsomeEcsGreen", 
    vpc=vpc_stack.vpc,
    tag="green",
    alb_sg=sgStack.myAlbSecurityGroup,
    ecs_sg=sgStack.myEcsSecurityGroup,
    cluster=ecsFgtClusterStack.myCluster,
    # repo_arn = "arn:aws:ecr:ap-northeast-2:499656329194:repository/ym_demo_ecr", 
    image_uri="public.ecr.aws/n3g9h1h6/ym-ecr/abp:green"
)    

app.synth()

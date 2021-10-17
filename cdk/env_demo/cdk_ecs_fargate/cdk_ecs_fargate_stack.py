from aws_cdk import (
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_ecr as ecr,
    aws_elasticloadbalancingv2 as elb,
    aws_ecs_patterns as ecs_patterns,
    aws_logs as logs,
    core
)


class CdkEcsFgtStack(core.Stack):
    


    def __init__(self, scope: core.Construct, id: str, tag: str, alb_healthcheck_uri: str, vpc, alb_sg, ecs_sg, cluster, image_uri: str, is_public: bool, container_entry_point: [], container_command: [], healthcheck_command: [], **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # define stack here       
        # referring https://pypi.org/project/aws-cdk.aws-ecs/
        
        ## from here, use public docker repository
        myImage=ecs.ContainerImage.from_registry(
               image_uri
        )

        
        # select private subnets
        mySubnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE)

        # define ALB, TG
        myTg=elb.ApplicationTargetGroup(
            self, "myTg_" + tag,
            vpc=vpc,
            port=8080,
            protocol=elb.ApplicationProtocol("HTTP"),
            deregistration_delay=core.Duration.seconds(30),
            health_check=elb.HealthCheck(
                healthy_threshold_count=2,
                interval=core.Duration.seconds(7),
                timeout=core.Duration.seconds(5),
                path=alb_healthcheck_uri,
                unhealthy_threshold_count=2
            ),
            target_type=elb.TargetType("IP")

        )

        myAlb=elb.ApplicationLoadBalancer(
            self, "myAlb_" + tag ,
            internet_facing=is_public,
            load_balancer_name="myAlb-" + tag,
            vpc=vpc,
            security_group=alb_sg
        )            
        
        myListener=myAlb.add_listener(
            "my80_" + tag,
            port=80,
            open=True
        )

        myListener.add_target_groups(
            "AddingTargetGroup", target_groups=[myTg]                        
        )

        ## To-Do register ECS task as a target on the targetgroup
        
        # [22/Mar/2021 14:07:36]
        myLogDriver=ecs.LogDriver.aws_logs(
            stream_prefix="/ecs/myEcsFgtTask" + tag,
            log_retention=logs.RetentionDays("ONE_WEEK"),
        )

        myTaskDefinition=ecs.FargateTaskDefinition(   ## define taskdefinition
            self, "myFgtAppTd_" + tag,
            cpu=1024,
            memory_limit_mib=2048,
            family="myTaskDef_"+tag,
        )


        ## To-Do log configuration is required
        myTaskDefinition.add_container(
            "addContainer_"+tag, image=myImage,
            #entry_point=["/bin/bash", "start.sh"],
            entry_point=container_entry_point,
            command=container_command,
            essential=True,
            port_mappings=[ecs.PortMapping(container_port=8080)],
            working_directory="/app",
            logging=myLogDriver,
            health_check=ecs.HealthCheck(
                    retries=3,                    
                    interval=core.Duration.seconds(15),                    
                    timeout=core.Duration.seconds(20),
                    command=healthcheck_command,
            )                        
        )

        myService=ecs.FargateService(
            self, "myFgtService_" + tag,
            service_name="my-awsome-service-"+tag,
            task_definition=myTaskDefinition,
            security_groups=[ecs_sg],
            cluster=cluster,
            vpc_subnets=mySubnets,
            desired_count=3,
            enable_ecs_managed_tags=True            
        )
        myService.attach_to_application_target_group(myTg)
        
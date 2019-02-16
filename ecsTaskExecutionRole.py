#=====================================================================================
###ecsTaskExecutionRole


import boto3
import json
import botocore


# handle credential

# [default]
aws_access_key_id = YOUR_ACCESS_KEY
aws_secret_access_key = YOUR_SECRET_KEY


# create role
rolepolicy = {
              "Version": "2012-10-17",
              "Statement": [
                {
                  "Sid": "",
                  "Effect": "Allow",
                  "Principal": {
                    "Service": "ecs-tasks.amazonaws.com"
                  },
                  "Action": "sts:AssumeRole"
                }
              ]
            }

newrolepolicy = json.dumps(rolepolicy)
response = client.create_role(
    Path='string',
    RoleName='ecsTaskExecutionRole-test',
    AssumeRolePolicyDocument=newrolepolicy
    )


#Create a policy


policyroledoc =  {
               "Version": "2012-10-17",
                "Statement": [
                  {
                  "Effect": "Allow",
                  "Action": 
                          [
                            "ecr:GetAuthorizationToken",
                            "ecr:BatchCheckLayerAvailability",
                            "ecr:GetDownloadUrlForLayer",
                            "ecr:BatchGetImage",
                            "logs:CreateLogStream",
                            "logs:PutLogEvents"
                            ],
                       
                  "Resource": "*"
                  }
              ]
            }

response = client.create_policy(
    PolicyName='AmazonECSTaskExecutionRolePolicy ',
    Path='/',
    PolicyDocument=policyroledoc
    )

# attach role with policy 

response = client.attach_role_policy(
    RoleName='ecsTaskExecutionRole-test',
    PolicyArn='arn:aws:iam::596040584433:policy/AmazonECSTaskExecutionRolePolicy'
)
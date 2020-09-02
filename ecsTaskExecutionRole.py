#=====================================================================================
###ecsTaskExecutionRole


import boto3
import json
import botocore
from botocore.exceptions import ClientError

# handle credential

EAST_SESSION = boto3.Session(region_name = 'us-east-2')
client = EAST_SESSION.client('iam')

# [default]
# aws_access_key_id = YOUR_ACCESS_KEY
# aws_secret_access_key = YOUR_SECRET_KEY


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

try:
  response = client.create_role(
      Path='/',
      RoleName='ecsTaskExecutionRole-test',
      AssumeRolePolicyDocument=newrolepolicy
      )
except ClientError as E:
    print ("Not able to create Role %s" %E)

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

policyroledoc = json.dumps(policyroledoc)

try:
  response = client.create_policy(
      PolicyName='AmazonECSTaskExecutionRolePolicy',
      Path='/',
      PolicyDocument=policyroledoc
      )
except ClientError as E:
    print "There is issue while creating policy. %s" %E
    


# attach role with policy 

response = client.attach_role_policy(
    RoleName='ecsTaskExecutionRole-test',
    PolicyArn='arn:aws:iam::596040584433:policy/AmazonECSTaskExecutionRolePolicy'
)
###AmazonEC2ContainerServiceforEC2Role


import boto3
import json
import botocore


#handle credential
EAST_SESSION = boto3.Session(region_name = 'us-east-2')
client = EAST_SESSION.client('iam')
# [default]
# aws_access_key_id = YOUR_ACCESS_KEY
# aws_secret_access_key = YOUR_SECRET_KEY


# create role

rolepolicy = {
  "Version": "2008-10-17",
  "Statement": [
    {
      "Sid": "",
      "Effect": "Allow",
      "Principal": {
        "Service": "ec2.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}

new_rolepolicy = json.dumps(rolepolicy)
response = client.create_role(
    Path='/',
    RoleName='AmazonEC2ContainerServiceforEC2Role-test',
    AssumeRolePolicyDocument=new_rolepolicy
    )



#Create a policy

policydoc = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "ecs:CreateCluster",
                "ecs:DeregisterContainerInstance",
                "ecs:DiscoverPollEndpoint",
                "ecs:Poll",
                "ecs:RegisterContainerInstance",
                "ecs:StartTelemetrySession",
                "ecs:UpdateContainerInstancesState",
                "ecs:Submit*",
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

new_rolepolicy = json.dumps(policydoc)
response = client.create_policy(
    PolicyName='AmazonEC2ContainerServiceforEC2Role',
    Path='/',
    PolicyDocument=new_rolepolicy
    )

# attach role policy 

response = client.attach_role_policy(
    RoleName='AmazonEC2ContainerServiceforEC2Role-test',
    PolicyArn='arn:aws:iam::596040584433:policy/AmazonEC2ContainerServiceforEC2Role'
)


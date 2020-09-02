###aws-elasticbeanstalk-ec2-role


import boto3
import json
import botocore


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
      "Effect": "Allow",
      "Principal": {
        "Service": "ec2.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}

newrolepolicy = json.dumps(rolepolicy)
response = client.create_role(
    Path='string',
    RoleName='aws-elasticbeanstalk-ec2-role',
    AssumeRolePolicyDocument=newrolepolicy,
    Description='elasticbeanstalk-ec2-role'
    )
    
#Create a policy

response = client.create_policy(
    PolicyName='AWSElasticBeanstalkWebTier',
    Path='/',
    PolicyDocument=,
    Description='string'
)

# attach role policy 

response = client.attach_role_policy(
    RoleName='aws-elasticbeanstalk-ec2-role-test',
    PolicyArn='arn:aws:iam::596040584433:policy/AWSElasticBeanstalkWebTier'
)

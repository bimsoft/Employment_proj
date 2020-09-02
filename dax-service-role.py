#=======================================================================
#need to update below scripts:

###dax-service-role


import boto3
import json
import botocore
from botocore.exceptions import ClientError


#self test handle credential
# EAST_SESSION = boto3.Session(region_name = 'us-east-2')
# client = EAST_SESSION.client('iam')

profilename = raw_input("Please enter your credential profile name: ")
rolename = raw_input(" Please enter  Role name: ")
policyname = raw_input(" Please enter Policy name: ")

profile = profilename
session = boto3.Session(profile_name=profile)
client = session.client('iam')


#[default]
#aws_access_key_id = YOUR_ACCESS_KEY
#aws_secret_access_key = YOUR_SECRET_KEY


# create role

rolepolicy = {
            "Version": "2012-10-17",
            "Statement": [
              {
                "Effect": "Allow",
                "Principal": {
                  "Service": "dax.amazonaws.com"
                },
                "Action": "sts:AssumeRole"
              }
            ]
          }

newrolepolicy = json.dumps(rolepolicy)

try:
  response = client.create_role(
      Path='/',
      RoleName=rolename,
      AssumeRolePolicyDocument=newrolepolicy,
      Description='string'
      )
except ClientError as E:
    print "There is issue while creating Role %s" %E

    
#Create a policy

policydoc = {
                "Version": "2012-10-17",
                "Statement": [
                {
                "Action": 
                  [
                  "dynamodb:*"
                  ],

                  "Effect": "Allow",
                  "Resource": 
                  [
                  "arn:aws:dynamodb::596040584433:*"
                  ]
                }
            ]

      }
newrolepolicy = json.dumps(policydoc)

try:
  response = client.create_policy(
      PolicyName=policyname,
      Path='/',
      PolicyDocument= newrolepolicy,
      Description='string'
  )
except ClientError as E:
    print "There is issue while creating policy %s" %E

# attach role policy 

policy_arn = "arn:aws:iam::596040584433:policy/"+policyname

response = client.attach_role_policy(
    RoleName=rolename,
    PolicyArn=policy_arn
)




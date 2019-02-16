#=======================================================================
#need to update below scripts:

###dax-service-role


import boto3
import json
import botocore


#handle credential

#[default]
aws_access_key_id = YOUR_ACCESS_KEY
aws_secret_access_key = YOUR_SECRET_KEY


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
response = client.create_role(
    Path='string',
    RoleName='Dax-service-role-test',
    AssumeRolePolicyDocument=newrolepolicy,
    Description='string'
    )
    
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
response = client.create_policy(
    PolicyName='dynamodb-all',
    Path='/',
    PolicyDocument= newrolepolicy,
    Description='string'
)

# attach role policy 

response = client.attach_role_policy(
    RoleName='dax-service-role-test',
    PolicyArn='arn:aws:iam::596040584433:policy/dynamodb-all'
)
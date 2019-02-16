#Script for config-service-role.

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
                  "Sid": "AssumeRole",
                  "Effect": "Allow",
                  "Principal": {
                    "Service": "config.amazonaws.com"
                  },
                  "Action": "sts:AssumeRole"
                }
              ]
            }

newrolepolicy = json.dumps(rolepolicy)           
response = client.create_role(
    Path='/', 
    RoleName='config-service-role-test',
    newrolepolicy = newrolepolicy
    )
    

#Create a policy

policydoc = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "cloudtrail:DescribeTrails",
                "ec2:Describe*",
                "config:Put*",
                "config:Get*",
                "config:List*",
                "config:Describe*",
                "cloudtrail:GetEventSelectors",
                "cloudtrail:GetTrailStatus",
                "cloudtrail:ListTags",
                "s3:GetObject",
                "iam:GetAccountAuthorizationDetails",
                "iam:GetAccountPasswordPolicy",
                "iam:GetAccountSummary",
                "iam:GetGroup",
                "iam:GetGroupPolicy",
                "iam:GetPolicy",
                "iam:GetPolicyVersion",
                "iam:GetRole",
                "iam:GetRolePolicy",
                "iam:GetUser",
                "iam:GetUserPolicy",
                "iam:GenerateCredentialReport",
                "iam:GetCredentialReport",
                "iam:ListAttachedGroupPolicies",
                "iam:ListAttachedRolePolicies",
                "iam:ListAttachedUserPolicies",
                "iam:ListEntitiesForPolicy",
                "iam:ListGroupPolicies",
                "iam:ListGroupsForUser",
                "iam:ListInstanceProfilesForRole",
                "iam:ListPolicyVersions",
                "iam:ListRolePolicies",
                "iam:ListUserPolicies",
                "iam:ListVirtualMFADevices",
                "elasticloadbalancing:DescribeLoadBalancers",
                "elasticloadbalancing:DescribeLoadBalancerAttributes",
                "elasticloadbalancing:DescribeLoadBalancerPolicies",
                "elasticloadbalancing:DescribeTags",
                "acm:DescribeCertificate",
                "acm:ListCertificates",
                "acm:ListTagsForCertificate",
                "rds:DescribeDBInstances",
                "rds:DescribeDBSecurityGroups",
                "rds:DescribeDBSnapshotAttributes",
                "rds:DescribeDBSnapshots",
                "rds:DescribeDBSubnetGroups",
                "rds:DescribeEventSubscriptions",
                "rds:ListTagsForResource",
                "rds:DescribeDBClusters",
                "s3:GetAccelerateConfiguration",
                "s3:GetBucketAcl",
                "s3:GetBucketCORS",
                "s3:GetBucketLocation",
                "s3:GetBucketLogging",
                "s3:GetBucketNotification",
                "s3:GetBucketPolicy",
                "s3:GetBucketRequestPayment",
                "s3:GetBucketTagging",
                "s3:GetBucketVersioning",
                "s3:GetBucketWebsite",
                "s3:GetLifecycleConfiguration",
                "s3:GetReplicationConfiguration",
                "s3:ListAllMyBuckets",
                "s3:ListBucket",
                "s3:GetEncryptionConfiguration",
                "redshift:DescribeClusterParameterGroups",
                "redshift:DescribeClusterParameters",
                "redshift:DescribeClusterSecurityGroups",
                "redshift:DescribeClusterSnapshots",
                "redshift:DescribeClusterSubnetGroups",
                "redshift:DescribeClusters",
                "redshift:DescribeEventSubscriptions",
                "redshift:DescribeLoggingStatus",
                "dynamodb:DescribeLimits",
                "dynamodb:DescribeTable",
                "dynamodb:ListTables",
                "dynamodb:ListTagsOfResource",
                "cloudwatch:DescribeAlarms",
                "application-autoscaling:DescribeScalableTargets",
                "application-autoscaling:DescribeScalingPolicies",
                "autoscaling:DescribeAutoScalingGroups",
                "autoscaling:DescribeLaunchConfigurations",
                "autoscaling:DescribeLifecycleHooks",
                "autoscaling:DescribePolicies",
                "autoscaling:DescribeScheduledActions",
                "autoscaling:DescribeTags",
                "lambda:GetFunction",
                "lambda:GetPolicy",
                "lambda:ListFunctions",
                "lambda:GetAlias",
                "lambda:ListAliases",
                "waf-regional:GetWebACLForResource",
                "waf-regional:GetWebACL",
                "cloudfront:ListTagsForResource",
                "guardduty:ListDetectors",
                "guardduty:GetMasterAccount",
                "guardduty:GetDetector",
                "codepipeline:ListPipelines",
                "codepipeline:GetPipeline",
                "codepipeline:GetPipelineState",
                "kms:ListKeys",
                "kms:GetKeyRotationStatus"
            ],
            "Resource": "*"
        }
    ]
}

newpolicydoc = json.dumps(rolepolicy)
response = client.create_policy(
    PolicyName='AWSConfigRole',
    PolicyDocument=newpolicydoc
    )


# attach role policy 
response = client.attach_role_policy(
    RoleName='config-service-role-test',
    PolicyArn='arn:aws:iam::596040584433:policy/AWSConfigRole'
)
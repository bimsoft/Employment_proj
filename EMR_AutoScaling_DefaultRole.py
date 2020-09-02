#Script for EMR_AutoScaling_DefaultRole.

import boto3
import json
import botocore

#handle credential
EAST_SESSION = boto3.Session(region_name = 'us-east-2')
client = EAST_SESSION.client('iam')

#[default]
# aws_access_key_id = YOUR_ACCESS_KEY
# aws_secret_access_key = YOUR_SECRET_KEY

# create role 

rolepolicy = {
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": [
          "elasticmapreduce.amazonaws.com",
          "application-autoscaling.amazonaws.com"
        ]
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
    
newrolepolicy = json.dumps(rolepolicy)
response = client.create_role(
    Path='/', 
    RoleName='EMR_AutoScaling_DefaultRole',
    AssumeRolePolicyDocument=newrolepolicy,
    )

#Create a policy

policydoc1 = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:List*",
                "s3:GetObject*",
                "s3:GetObjectVersion",
                "s3:PutObject",
                "s3:GetObjectAcl",
                "s3:PutObjectAcl",
                "s3:GetObjectVersionAcl",
                "s3:DeleteObject",
                "s3:DeleteObjectVersion",
                "s3:AbortMultipartUpload",
                "s3:GetObjectTorrent",
                "s3:GetObjectVersionTorrent",
                "s3:RestoreObject",
                "s3:GetBucketPolicy",
                "s3:GetBucketVersioning",
                "s3:GetBucketLocation",
                "s3:GetBucketWebsite",
                "s3:GetLifecycleConfiguration"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "kms:CreateAlias",
                "kms:CreateKey",
                "kms:DeleteAlias",
                "kms:Describe*",
                "kms:GenerateRandom",
                "kms:List*",
                "kms:Get*",
                "kms:Encrypt",
                "kms:Decrypt",
                "kms:ReEncrypt",
                "kms:GenerateDataKey"
            ],
            "Resource": "*"
        }
    ]
}

#Create a policy
newpolicydoc1 = json.dumps(policydoc1)
response = client.create_policy(
    PolicyName='bu-s3-consumer',
    PolicyDocument=newpolicydoc1
    )



policydoc2 = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "BlanketDeny",
            "Effect": "Deny",
            "Action": [
                "acm:RequestCertificate",
                "aws-portal:*",
                "budgets:*",
                "clouddirectory:*",
                "cloudhsm:*",
                "cloudsearch:*Domain*",
                "codebuild:*",
                "codecommit:*",
                "codestar:*",
                "cur:*",
                "devicefarm:*",
                "discovery:*",
                "ds:*",
                "gamelift:*",
                "iot:*",
                "lightsail:*",
                "mechanicalturk:*",
                "mobileanalytics:*",
                "mobilehub:*",
                "organizations:*",
                "polly:*",
                "ses:*",
                "workdocs:*",
                "workmail:*",
                "workspaces:*"
            ],
            "Resource": "*"
        },
        {
            "Sid": "TargetedDeny",
            "Effect": "Deny",
            "Action": [
                "cloudtrail:CreateTrail",
                "cloudtrail:DeleteTrail",
                "cloudtrail:StartLogging",
                "cloudtrail:StopLogging",
                "cloudtrail:UpdateTrail",
                "config:DeleteConfigurationRecorder",
                "config:DeleteDeliveryChannel",
                "config:StopConfigurationRecorder",
                "directconnect:Allocate*",
                "directconnect:Confirm*",
                "directconnect:Create*",
                "directconnect:Delete*",
                "ec2:AcceptVpcPeeringConnection",
                "ec2:AllocateAddress",
                "ec2:AllocateHosts",
                "ec2:AssociateAddress",
                "ec2:AssociateDhcpOptions",
                "ec2:AttachClassicLinkVpc",
                "ec2:AttachInternetGateway",
                "ec2:AttachVpnGateway",
                "ec2:CancelReservedInstancesListing",
                "ec2:CreateCustomerGateway",
                "ec2:CreateDhcpOptions",
                "ec2:CreateInternetGateway",
                "ec2:CreateNatGateway",
                "ec2:CreateReservedInstancesListing",
                "ec2:CreateRoute*",
                "ec2:CreateVp*",
                "ec2:DeleteCustomerGateway",
                "ec2:DeleteDhcpOptions",
                "ec2:DeleteInternetGateway",
                "ec2:DeleteNatGateway",
                "ec2:DeleteRoute*",
                "ec2:DeleteVp*",
                "ec2:DetachClassicLinkVpc",
                "ec2:DetachInternetGateway",
                "ec2:DetachVpnGateway",
                "ec2:Disable*",
                "ec2:DisassociateAddress",
                "ec2:EnableVgwRoutePropagation",
                "ec2:EnableVpcClassicLink",
                "ec2:ImportInstance",
                "ec2:ImportVolume",
                "ec2:ModifyReservedInstances",
                "ec2:ModifySubnetAttribute",
                "ec2:ModifyVpcAttribute",
                "ec2:PurchaseReservedInstancesOffering",
                "ec2:PurchaseScheduledInstances",
                "ec2:RejectVpcPeeringConnection",
                "ec2:ReleaseAddress",
                "ec2:ReleaseHosts",
                "ec2:ReplaceRoute",
                "ec2:RunScheduledInstances",
                "route53:AssociateVPCWithHostedZone",
                "route53:ChangeResourceRecordSets",
                "route53:ChangeTagsForResource",
                "route53:Create*",
                "route53:Delete*",
                "route53:DisassociateVPCFromHostedZone",
                "route53domains:*",
                "route53:Update*",
                "ses:Delete*",
                "ses:Send*",
                "ses:SetIdentity*",
                "ses:Verify*",
                "storagegateway:ActivateGateway",
                "storagegateway:AddCache",
                "storagegateway:AddUploadBuffer",
                "storagegateway:AddWorkingStorage",
                "storagegateway:Cancel*",
                "storagegateway:Create*",
                "storagegateway:Delete*",
                "storagegateway:DisableGateway",
                "storagegateway:RefreshCache",
                "storagegateway:Retrieve*",
                "storagegateway:ShutdownGateway",
                "storagegateway:StartGateway",
                "storagegateway:Update*",
                "sts:GetFederationToken"
            ],
            "Resource": "*"
        },
        {
            "Sid": "BlanketIAMDeny",
            "Effect": "Deny",
            "Action": [
                "iam:*CreateAccount*",
                "iam:*DeleteAccount*",
                "iam:*OpenIdConnect*",
                "iam:*SAMLProvider",
                "iam:*UpdateAccount*",
                "iam:AddUserToGroup",
                "iam:Attach*Policy",
                "iam:ChangePassword",
                "iam:CreateGroup",
                "iam:CreateLoginProfile",
                "iam:CreatePolicy*",
                "iam:CreateRole",
                "iam:CreateUser",
                "iam:CreateVirtualMFADevice",
                "iam:DeactivateMFADevice",
                "iam:DeleteGroup",
                "iam:DeleteGroupPolicy",
                "iam:DeleteInstanceProfile",
                "iam:DeleteLoginProfile",
                "iam:DeletePolicy*",
                "iam:DeleteRole*",
                "iam:DeleteUser*",
                "iam:DeleteVirtualMFADevice",
                "iam:Detach*Policy",
                "iam:EnableMFADevice",
                "iam:Put*Policy",
                "iam:RemoveRoleFromInstanceProfile",
                "iam:RemoveUserFromGroup",
                "iam:ResyncMFADevice",
                "iam:SetDefaultPolicyVersion",
                "iam:UpdateAssumeRolePolicy",
                "iam:UpdateGroup",
                "iam:UpdateLoginProfile",
                "iam:UpdateUser"
            ],
            "Resource": "*"
        },
        {
            "Sid": "DenyEIPs",
            "Effect": "Deny",
            "Action": [
                "ec2:AllocateAddress",
                "ec2:AssociateAddress",
                "ec2:DisassociateAddress"
            ],
            "Resource": "*"
        }
    ]
}
    
#Create a policy
newpolicydoc2 = json.dumps(policydoc2)
response = client.create_policy(
    PolicyName='awsiam-sauce',
    PolicyDocument=newpolicydoc2
    )



policydoc3 = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "AllowLaunchOnlyFromApprovedImages",
            "Effect": "Deny",
            "Action": "ec2:RunInstances",
            "Resource": "arn:aws:ec2:us-east-1::image/ami-*",
            "Condition": {
                "ForAnyValue:StringNotLike": {
                    "ec2:Owner": [
                        "277688789493",
                        "amazon",
                        "aws-marketplace",
                        "737859062117",
                        "394136139437",
                        "851093456999",
                        "335031091084",
                        "207456136159",
                        "028557712108",
                        "164996153968",
                        "533600275369",
                        "930136447543",
                        "658312218119",
                        "687831498517",
                        "201245860548",
                        "596040584433",
                        "493917785438",
                        "378058653094",
                        "901455435209",
                        "652668783151",
                        "988201728534",
                        "669990426999",
                        "142986109290",
                        "679593333241",
                        "309956199498"
                    ]
                }
            }
        },
        {
            "Sid": "ActionsForInstanceLaunchAndMgmnt",
            "Effect": "Deny",
            "Action": [
                "ec2:BundleInstance",
                "ec2:CancelBundleTask",
                "ec2:MonitorInstances",
                "ec2:CreatePlacementGroup",
                "ec2:ModifyInstanceAttribute",
                "ec2:ReportInstanceStatus",
                "ec2:RunInstances",
                "ec2:StartInstances",
                "ec2:StopInstances",
                "ec2:TerminateInstances",
                "ec2:UnmonitorInstances",
                "ec2:ResetInstanceAttribute",
                "ec2:DeletePlacementGroup",
                "ec2:RebootInstances"
            ],
            "Resource": [
                "arn:aws:ec2:us-east-1:596040584433:subnet/subnet-5ef9b505",
                "arn:aws:ec2:us-east-1:596040584433:subnet/subnet-58f9b503",
                "arn:aws:ec2:us-east-1:596040584433:subnet/subnet-fb94c5d6",
                "arn:aws:ec2:us-east-1:596040584433:subnet/subnet-f494c5d9"
            ],
            "Condition": {
                "StringLike": {
                    "ec2:ResourceTag/csadmin": "csadmin"
                }
            }
        },
        {
            "Sid": "ProtectCSAdminResources",
            "Effect": "Deny",
            "Action": [
                "ec2:AttachVolume",
                "ec2:CreateSnapshot",
                "ec2:CreateVolume",
                "ec2:DeleteVolume",
                "ec2:DetachVolume",
                "ec2:EnableVolumeIo",
                "ec2:ModifyVolumeAttribute",
                "ec2:CopySnapshot",
                "ec2:DeleteSnapshot",
                "ec2:ModifySnapshotAttribute",
                "ec2:ResetSnapshotAttribute"
            ],
            "Resource": "*",
            "Condition": {
                "StringLike": {
                    "ec2:ResourceTag/csadmin": "csadmin"
                }
            }
        },
        {
            "Sid": "ProtectPurpleSpider",
            "Effect": "Deny",
            "Action": "ec2:*SecurityGroup*",
            "Resource": "*",
            "Condition": {
                "StringLike": {
                    "ec2:ResourceTag/aws:cloudformation:stack-name": "purple-spider"
                }
            }
        },
        {
            "Sid": "IAMPassroleDeny",
            "Effect": "Deny",
            "Action": "iam:PassRole",
            "Resource": [
                "arn:aws:iam::596040584433:role/admin-to-gecc",
                "arn:aws:iam::596040584433:role/aws-config-service-role",
                "arn:aws:iam::596040584433:role/awsiam2",
                "arn:aws:iam::596040584433:role/bu-iam-admin",
                "arn:aws:iam::596040584433:role/cirt",
                "arn:aws:iam::596040584433:role/cloud-admin",
                "arn:aws:iam::596040584433:role/cloud-support",
                "arn:aws:iam::596040584433:role/iam-admin-to-gecc",
                "arn:aws:iam::596040584433:role/monitor-and-tag-to-gecc",
                "arn:aws:iam::596040584433:role/read-only-to-gecc",
                "arn:aws:iam::596040584433:role/reaperbot",
                "arn:aws:iam::596040584433:role/super-admin-to-gecc",
                "arn:aws:iam::596040584433:role/trusted-iam-admin",
                "arn:aws:iam::596040584433:role/trusted-super-admin",
                "arn:aws:iam::596040584433:role/vpc_flow_to_logs",
                "arn:aws:iam::596040584433:role/api-read-to-gecc",
                "arn:aws:iam::596040584433:role/api-2-read-to-gecc",
                "arn:aws:iam::596040584433:role/api-dev-read-to-gecc",
                "arn:aws:iam::596040584433:role/p-hpa",
                "arn:aws:iam::596040584433:role/p-support",
                "arn:aws:iam::596040584433:role/p-platformadmin",
                "arn:aws:iam::596040584433:role/p-engineering",
                "arn:aws:iam::596040584433:role/p-architect",
                "arn:aws:iam::*:role/cs/*"
            ]
        }
    ]
}

newpolicydoc3 = json.dumps(policydoc3)
response = client.create_policy(
    PolicyName='awsiam-sauce-the-sequel',
    PolicyDocument=newpolicydoc3
    )

    #Create a policy

policydoc4 = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Action": [
                "cloudwatch:DescribeAlarms",
                "elasticmapreduce:ListInstanceGroups",
                "elasticmapreduce:ModifyInstanceGroups"
            ],
            "Effect": "Allow",
            "Resource": "*"
        }
    ]
}
    
newpolicydoc4 = json.dumps(policydoc4)
response = client.create_policy(
    PolicyName='bu-s3-consumer',
    PolicyDocument=newpolicydoc4
    )

# attach role policy 
response = client.attach_role_policy(
    RoleName='EMR_AutoScaling_DefaultRole-test',
    PolicyArn='arn:aws:iam::596040584433:policy/awsiam-sauce'
)

response = client.attach_role_policy(
    RoleName='EMR_AutoScaling_DefaultRole-test',
    PolicyArn='arn:aws:iam::596040584433:policy/awsiam-sauce'
)

response = client.attach_role_policy(
    RoleName='EMR_AutoScaling_DefaultRole-test',
    PolicyArn='arn:aws:iam::596040584433:policy/awsiam-sauce-the-sequel'
)

response = client.attach_role_policy(
    RoleName='EMR_AutoScaling_DefaultRole-test',
    PolicyArn='arn:aws:iam::596040584433:policy/mr-autoscaling'
)


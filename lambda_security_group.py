import json
import boto3
from botocore.exceptions import ClientError
from pprint import pprint as pp

def lambda_handler(event, context):
    # TODO implement
    return create_security_group()

def create_security_group():
    ec2 = boto3.client('ec2')
    response = ec2.describe_vpcs()
    vpc_id = response.get('Vpcs', [{}])[0].get('VpcId', '')
    security_group_id_1 = ""
    security_group_id_2 = ""
    
    #  Create Security Group SECURITY_GROUP_ONE
    try:
        response = ec2.create_security_group(GroupName='SECURITY_GROUP_ONE',
                                             Description='FIRST',
                                             VpcId=vpc_id)
        security_group_id_1 = response['GroupId']
        print('Security Group Created %s in vpc %s.' % (security_group_id_1, vpc_id))
        
        #  Inbound rule 1
        ingress_data = ec2.authorize_security_group_ingress(
            GroupId=security_group_id_1,
            IpPermissions=[
                {'IpProtocol': 'tcp',
                 'FromPort': 80,
                 'ToPort': 80,
                 'IpRanges': [{'CidrIp': '10.229.80.0/22'}]},
                {'IpProtocol': 'tcp',
                 'FromPort': 6273,
                 'ToPort': 6273,
                 'IpRanges': [{'CidrIp': '10.229.80.0/22'}]},
                {'IpProtocol': 'tcp',
                 'FromPort': 8008,
                 'ToPort': 8014,
                 'IpRanges': [{'CidrIp': '10.229.80.0/22'}]},
                {'IpProtocol': 'tcp',
                 'FromPort': 8008,
                 'ToPort': 8013,
                 'IpRanges': [{'CidrIp': '10.38.9.0/24'}]}
            ])
        print 'Ingress for security group SECURITY_GROUP_ONE Successfully Set %s' % ingress_data
        
        
    except ClientError as e:
        print 'Failed... Unable to create a new security group ONE: faultCode=%s'% (e)
        
    #  Create Security Group SECURITY_GROUP_TWO
    try:
        response = ec2.create_security_group(GroupName='SECURITY_GROUP_TWO',
                                             Description='SECOND',
                                             VpcId=vpc_id)
        security_group_id_2 = response['GroupId']
        print('Security Group Created %s in vpc %s.' % (security_group_id_2, vpc_id))
        
        #  Inbound rule 1
        ingress_data = ec2.authorize_security_group_ingress(
            GroupId=security_group_id_2,
            IpPermissions=[
                {'IpProtocol': 'tcp',
                 'FromPort': 80,
                 'ToPort': 80,
                 'IpRanges': [{'CidrIp': '10.229.80.0/22'}]},
                {'IpProtocol': 'tcp',
                 'FromPort': 6273,
                 'ToPort': 6273,
                 'IpRanges': [{'CidrIp': '10.229.80.0/22'}]},
                {'IpProtocol': 'tcp',
                 'FromPort': 8008,
                 'ToPort': 8014,
                 'IpRanges': [{'CidrIp': '10.229.80.0/22'}]},
                {'IpProtocol': 'tcp',
                 'FromPort': 8008,
                 'ToPort': 8013,
                 'IpRanges': [{'CidrIp': '10.38.9.0/24'}]}
            ])
        print 'Ingress for security group SECURITY_GROUP_TWO Successfully Set %s' % ingress_data
        
        
    except ClientError as e:
        print 'Failed... Unable to create a new security group two: faultCode=%s'% (e)
    

#sga-rds
# This script is Triggerred from Cloudwatch
# Check the Cloudwatch Event for the launch of RDS instance and Create a default security group if needed.
# It is creating object of SNS, RDS, ec2 client and EC2 resource
# rds_sga() is function called by lambda
# It gets DBidentifier and ARN of it. THrough the DB instance it find their corresponding VPC id and DB instnce status
# If Event is to createDB related and it is test instance then it sends message in to AWS SQS to create
# If defined DB instance is already available then list out the tags of RDS same.
# It looks for tag name of RDS if it is tag'key value is UAI then it created Default Security Group
# After that it finds IF of security Group ID that us associated with RDS
# after checking all the SGs on the RDS instance, if nothing matches then create default SG or if exists then it associate with that instance


# Next script also does similar kind of stuff means creating default Security group.



import os
import boto3

# create clients for later
sns = boto3.client('sns')
rds = boto3.client('rds')
ec2 = boto3.client('ec2')
ec2r = boto3.resource('ec2')

def rds_sga(event,context):    
    print(event)
    try:
        event_name = event['detail']['eventName']
    except:
        event_name = 'none'
    try:# CreateDBinstance/ModifyDBInstance
        dbii = event['detail']['requestParameters']['dBInstanceIdentifier']
        arn = event['detail']['responseElements']['dBInstanceArn']
    except:
        try:# AddTagsToResource
            dbii = event['detail']['requestParameters']['resourceName'].rpartition(':')[2]
            arn = event['detail']['requestParameters']['resourceName']
        except:   # SQS Message
            dbii = event['Records'][0]['body'].rpartition(',')[0]
            arn = event['Records'][0]['body'].rpartition(',')[2]
            event_name = 'SQS'
    instance = rds.describe_db_instances(DBInstanceIdentifier=dbii)
    vpc_id = instance['DBInstances'][0]['DBSubnetGroup']['VpcId']
    db_status = instance['DBInstances'][0]['DBInstanceStatus']
    # checks for event name
    if(event_name == 'none'):
        print('No event to process.')
    elif(event_name == 'CreateDBInstance' and dbii == os.environ['test_instance'] ):
        print('RDS database might be unavailable or does not need to be checked.')
        client = boto3.client('sqs')
        response = client.send_message(
            QueueUrl='https://sqs.us-east-1.amazonaws.com/596040584433/sga-rds',
            MessageBody=dbii + ',' + arn
        )
        print('Sent a message to the SQS queue for: ' +dbii + '\n' + str(response))
    elif(db_status == 'available' and dbii == os.environ['test_instance']): 
        print('Event: ' + event_name + ' detected on: ' + arn)
        if event_name == 'AddTagsToResource':
            print('--' + str(event['detail']['requestParameters']['tags']))
        tags = rds.list_tags_for_resource(
            ResourceName=arn
        )
        # loops through all the tags 
        print('Checking for UAI tag.')
        for tag in tags['TagList']:
            if (tag['Key'].upper() == 'UAI'):
                uai_tags = tag['Value'].split('-')
                total_tags = len(uai_tags)
                default_sg_name = str(tag['Value']).upper() + "_DefaultAppSG"
                print('Default App SG required on instance: ' + default_sg_name)
                # get list of existing SGs and look for a DefaultAppSG
                instance_sgs = instance['DBInstances'][0]['VpcSecurityGroups']
                #print(instance_sgs)
                all_sg_ids = [sg['VpcSecurityGroupId'] for sg in instance_sgs]   
                #print(all_sg_ids)
                sg_id = 0
                match_found = 0
                for sg in instance_sgs:
                    sub_sg_id = sg['VpcSecurityGroupId']
                    sg = ec2r.SecurityGroup(sub_sg_id)
                    if str(sg.group_name) == default_sg_name:
                        match_found = 1
                        print('NO ACTION REQUIRED -- The RDS instance already has a DefaultAppSG security group attached: ' + sg.group_name + ' : ' + sub_sg_id)
                # after checking all the SGs on the instance, if nothing matches...
                if match_found == 0:
                    result = does_the_sg_exist(default_sg_name)
                    if  result == 0:
                        print('ACTION REQUIRED -- Did not find a default application security group.')
                        create_default_sg(instance,default_sg_name,uai_tags)
                    else:
                        attach_sg_to_instance(result,instance)                     
        check_common_sg(instance)

# if extist, return sg_id, if not, return 0
def does_the_sg_exist(default_sg_name):
    print('CHECKING for: ' + default_sg_name)
    try:
        describe_sg = ec2.describe_security_groups(
                    Filters=[
                        {
                            'Name': 'group-name',
                            'Values': [
                                default_sg_name,
                            ]
                        }
                    ]
        )
        #print('Describe Security Groups: ' + str(describe_sg))
        sg_name = describe_sg['SecurityGroups'][0]['GroupName']
        #print('--We found: ' + sg_name)
        if sg_name == default_sg_name:
            print('--Found existing Default SG.')
            return describe_sg['SecurityGroups'][0]['GroupId']
        else:
            print('--Found no existing Default SG.')
            return 0
    except:
        print('--Found no existing Default SG.')
        return 0

def add_sg_rules(sg_id,sg):
    # add that UAI's default security group to default SG
    # lookup a list of security groups matching that name
    print('Adding ' + sg_id + ' to ' + str(sg.group_id)) 
    # 2a. attach the rules using the UAI's security group ID 
    egress_rule = sg.authorize_egress(
        DryRun=False,
        IpPermissions=[
            {
                'IpProtocol':'-1',
                'UserIdGroupPairs': [
                    {
                        'GroupId': sg_id
                    }
                ]
            }
        ]
    )
    print('--Added Egress rule.')
    ingress_rule = sg.authorize_ingress(
        DryRun=False,
        IpPermissions=[
            {
                'IpProtocol':'-1',
                'IpRanges':[],
                'UserIdGroupPairs': [
                    {
                        'GroupId': sg_id
                    }
                ]
            }
        ]
    )
    print('--Added Ingress Rule.')
    try:
        remove_cidr_rule = sg.revoke_egress(
            IpPermissions=[
                {
                    'IpProtocol':'-1',
                    'IpRanges': [
                        {
                            'CidrIp': '0.0.0.0/0'
                        }
                    ]
                }
            ]
        )
        print('--Removed CIDR Egress rule (0.0.0.0/0)')
    except:
        print('--No CIDR Egress rule (0.0.0.0/0) to remove.')
    #print('Rules: \n--' + str(sg.ip_permissions) + '\n--' + str(sg.ip_permissions_egress))

def attach_sg_to_instance(sg_id,instance):
    dbii = instance['DBInstances'][0]['DBInstanceIdentifier']
    print('Attaching SG(' + str(sg_id) + ') to instance: ' + dbii)
    all_sg_ids = instance['DBInstances'][0]['VpcSecurityGroups']
    # create list of SG IDs
    all_sg_ids = [sg['VpcSecurityGroupId'] for sg in all_sg_ids]   
    print('--Security Groups BEFORE: ' + str(all_sg_ids))
    # add new SG ID to list
    all_sg_ids.append(sg_id)
    modify_sg_ids = rds.modify_db_instance(
        DBInstanceIdentifier=dbii,
        VpcSecurityGroupIds=all_sg_ids
    )
    new_sg_ids = modify_sg_ids['DBInstance']['VpcSecurityGroups']
    new_sg_ids = [sg['VpcSecurityGroupId'] for sg in new_sg_ids]
    print('--Security Groups AFTER: ' + str(new_sg_ids))
    
def create_default_sg(instance,default_sg_name,uai_tags):
    vpc_id = instance['DBInstances'][0]['DBSubnetGroup']['VpcId']
    # 1. create security group
    print('Creating security group: ' + default_sg_name)
    # create default group that can be used for multiple or single UAIs
    create_default_sg = ec2.create_security_group(
        Description='default security group to allow ingres/egress from same UAIs.',
        GroupName=default_sg_name,
        VpcId=vpc_id
    )
    # get Default SG ID from the create function
    default_sg_id = create_default_sg['GroupId']
    print('--New Default SG ID: ' + default_sg_id)
    # create SG instance for use later
    default_sg = ec2r.SecurityGroup(default_sg_id)
    # 2. Add rules/groups to new default security group. 
    # MULTIPLE UAIs
    if len(uai_tags) > 1:
        print('Multiple UAIs detected. Adding multiple groups beneath default security group.')
        # loop through UAIs
        for uai in uai_tags:
            # create sub-security group from each UAI        
            sub_sg_name = uai.upper() + '_DefaultAppSG'
            # checking if sub-security group exists
            exists = does_the_sg_exist(sub_sg_name)   
            # create security group if exists=0
            if exists == 0:
                print('--Did not find a required subsecurity group for this UAI: ' + uai)
                print('--Creating security group: ' + sub_sg_name)
                create_sub_sg = ec2.create_security_group(
                    Description='Default security group to allow ingres/egress from same UAIs.',
                    GroupName=sub_sg_name,
                    VpcId=vpc_id
                )
                sub_sg_id = create_sub_sg['GroupId']
                sub_sg = ec2r.SecurityGroup(sub_sg_id)
                add_sg_rules(sub_sg_id,sub_sg)
                print('----Sub-group creation complete.')   
                add_sg_rules(sub_sg_id,default_sg)             
                print('------Added sub-group to default group.')
            # or just add sub-security group to default security group
            else:
                add_sg_rules(exists,default_sg)
    # SINGLE UAI
    else:    
        print('Single UAI Detected.')
        # attach the rules using the UAI's security group ID 
        add_sg_rules(default_sg_id,default_sg)
        print('--Add rules to default security group.')
    # Print New Default Security Group with/without sub-security groups attached
    print('Default Security Group Complete: ' + str(default_sg.group_name) + '-' + str(default_sg.group_id))
    # NEWWWW Attach group to instance
    attach_sg_to_instance(default_sg_id,instance)

def check_common_sg(instance):    
    print('Checking for Engine specific Security Groups:') 
    all_sg_ids = instance['DBInstances'][0]['VpcSecurityGroups']
    all_sg_ids = [sg['VpcSecurityGroupId'] for sg in all_sg_ids]   
    print('Security Groups on instance: ' + str(all_sg_ids))
    common_sg_id = os.environ['common_sg_id']
    if common_sg_id in all_sg_ids:                                         
        print('The Common Security Group is already in attached to the instance. \nDone.')
    else:
        print('The Common Security Group is not attached to instance. Attaching ' + common_sg_id + ' now.')
        attach_sg_to_instance(common_sg_id,instance)
        print('Complete.')

def check_sg_attached(instance,sg_id):    
    all_sg_ids = instance['DBInstances'][0]['VpcSecurityGroups']
    all_sg_ids = [sg['VpcSecurityGroupId'] for sg in all_sg_ids]   
    print('Security Groups on instance: ' + str(all_sg_ids))
    db_sg_id = engines[engine]
    if sg in all_sg_ids:                                         
        print('The ' + engine + ' Security Group is already in attached to the instance. \nDone.')
    else:
        print('The ' + engine + ' Security Group is not attached to instance. Attaching ' + db_sg_id + ' now.')
        attach_sg_to_instance(db_sg_id,instance)
        print('Complete.')
========================================================================================
#ec2
# Trigger: Cloudwatch and SQS
# Check the Cloudwatch Event and Create a default security group if needed.

import boto3
import os

# create clients for later
sns = boto3.client('sns')
ec2 = boto3.client('ec2')
ec2_resource = boto3.resource('ec2')

def ec2_sga(event,context):
    print(event)
    # Checks for all possibilities of resourceIds. 
    try:
        # CreateTags
        resource_id = event['detail']['requestParameters']['resourcesSet']['items'][0]['resourceId']
    except:
        try:
            # SQS message
            resource_id = event['Records'][0]['body']
        except:
            # RunInstances
            resource_id = event['detail']['responseElements']['instancesSet']['items'][0]['instanceId']
            # Send message to SQS to delay running the UAI checker
            client = boto3.client('sqs')
            response = client.send_message(
                QueueUrl='https://sqs.us-east-1.amazonaws.com/596040584433/sga-ec2',
                MessageBody=resource_id
            )
            print('Sent a message to the SQS queue: ' + str(response))
    

    # checks for resource ID that pertains to an EC2 instance 
    if (resource_id.startswith('i-') and resource_id == os.environ['test_instance']): ### ONLY FOR TESTING
    #if (resource_id.startswith('i-')): ### this will capture all EC2 events
        print('Instance ID Detected: ' + resource_id)
        instance = ec2_resource.Instance(resource_id)
        
        # finds tags area
        try:
            tags = event['detail']['requestParameters']['tagSet']['items']
        except:
            response = ec2.describe_instances(
                Filters=[
                    {
                        'Name': 'instance-id',
                        'Values': [
                            resource_id
                        ]
                    },
                ]
            )
            try:
                tags = response['Reservations'][0]['Instances'][0]['Tags']
            except:
                print('No tags found. We should probably send an email to tell someone or else the VM will get stopped.')
                return 0



        # loops through all the tags. Looks ugly because CloudTrail and SQS have different key formats.
        for tag in tags:
            try:
                key = str(tag['key']).upper()
            except:
                key = str(tag['Key']).upper()
            if (key == 'UAI'):
                try:
                    uai_tags = tag['value'].split('-')
                    default_sg_name = str(tag['value']).upper() + "_DefaultAppSG"
                except:
                    uai_tags = tag['Value'].split('-')
                    default_sg_name = str(tag['Value']).upper() + "_DefaultAppSG"
                total_tags = len(uai_tags)

                # look for a matching DefaultAppSG security group on the instance
                match_found = 0
                
                security_groups = instance.security_groups
                for group in security_groups:
                    group_name = (group['GroupName'])
                    if group_name == default_sg_name:
                        match_found = 1
                        print(resource_id + ' already has a DefaultAppSG security group attached (' + group_name + ').')
                        print('NO ACTION REQUIRED.')
                if match_found == 0:
                    if does_the_sg_exist(default_sg_name) == 1:
                        attach_sg_to_instance(default_sg_name,instance)
                    else:
                        fix_security_groups(instance,default_sg_name,uai_tags)
        check_common_sg(instance)


def does_the_sg_exist(default_sg_name):
    print('We are checking for: ' + default_sg_name)
    try:
        describe_sg = ec2.describe_security_groups(
                    Filters=[
                        {
                            'Name': 'group-name',
                            'Values': [
                                default_sg_name,
                            ]
                        }
                    ]
        )
        print('Describe Security Groups: ' + str(describe_sg))
        sg_name = describe_sg['SecurityGroups'][0]['GroupName']
        print('We found: ' + sg_name)
        if sg_name == default_sg_name:
            print('Found existing Default SG.')
            return 1
        else:
            print('Found no existing Default SG.')
            return 0
    except:
        print('Found no existing Default SG.')
        return 0
        

def attach_sg_to_instance(sg_name,instance):
    print('Attaching SG(' + sg_name + ') to instance: ' + instance.id)

    describe_sg = ec2.describe_security_groups(
                Filters=[
                    {
                        'Name': 'group-name',
                        'Values': [
                            sg_name,
                        ]
                    }
                ]
    )
    --print(describe_sg)
            
    # get the UAI's security group ID
    sg_id = describe_sg['SecurityGroups'][0]['GroupId']

    all_sg_ids = [sg['GroupId'] for sg in instance.security_groups]   

    ----print(all_sg_ids)

    all_sg_ids.append(sg_id)
    
    instance.modify_attribute(Groups=all_sg_ids)
    
    new_all_sg_ids = [sg['GroupId'] for sg in instance.security_groups]
    
    ------print('ADDED Security Group(' + sg_id + ') to Instance(' + instance.instance_id + '). List of sub-groups: ' + str(new_all_sg_ids))


def fix_security_groups(instance,default_sg_name,uai_tags):
    
    # 1. create security group
    print('Creating security group: ' + default_sg_name)
    instance_vpc_id = instance.vpc_id
    create_default_sg = ec2.create_security_group(
        Description='default security group to allow ingres/egress from same UAIs.',
        GroupName=default_sg_name,
        VpcId=instance_vpc_id,
        DryRun=False
    )
    print('Succeeded. ')

    # get Default SG ID from the create function
    default_sg_id = create_default_sg['GroupId']
    print('New Default SG ID: ' + default_sg_id)
    default_sg = ec2_resource.SecurityGroup(default_sg_id)

    # 2. Add rules/groups to new security group. If statement for single/multiple UAIs
    # MULTIPLE UAI
    if len(uai_tags) > 1:
        print('Multiple UAIs detected. Adding multiple groups beneath default security group.')
        # loop through UAIs
        for uai in uai_tags:
            # create 'assumed' security group from each UAI        
            temp_sg_name = uai.upper() + '_DefaultAppSG'   
            
            # try to get the security group ID, if not create one and get it
            try:
                describe_sg = ec2.describe_security_groups(
                    Filters=[
                        {
                            'Name': 'group-name',
                            'Values': [
                                temp_sg_name,
                            ]
                        }
                    ]
                )
                temp_sg_id = describe_sg['SecurityGroups'][0]['GroupId']
            except:
                temp_sg_id = create_sg(temp_sg_name,instance_vpc_id)

            print('adding ' + temp_sg_name + '(' + temp_sg_id + ') to ' + default_sg_name + '(' + default_sg_id + ')') 

            # 2a. attach the rules using the UAI's security group ID 
            egress_rule = default_sg.authorize_egress(
                DryRun=False,
                IpPermissions=[
                    {
                        'IpProtocol':'-1',
                        'UserIdGroupPairs': [
                            {
                                'GroupId': temp_sg_id
                            }
                        ]
                    }
                ]
            )
            print('--Added Egress rule.')

            ingress_rule = default_sg.authorize_ingress(
                DryRun=False,
                IpPermissions=[
                    {
                        'IpProtocol':'-1',
                        'IpRanges':[],
                        'UserIdGroupPairs': [
                            {
                                'GroupId': temp_sg_id
                            }
                        ]
                    }
                ]
            )
            print('--Added Ingress Rule.')
    # SINGLE UAI
    else:    
        print('Single UAI Detected.')
        # attach the rules using the UAI's security group ID 
        egress_rule = default_sg.authorize_egress(
            DryRun=False,
            IpPermissions=[
                {
                    'IpProtocol':'-1',
                    'UserIdGroupPairs': [
                        {
                            'GroupId': default_sg_id
                        }
                    ]
                }
            ]
        )
        print('--Added Egress rule.')
        ingress_rule = default_sg.authorize_ingress(
            DryRun=False,
            IpPermissions=[
                {
                    'IpProtocol':'-1',
                    'IpRanges':[],
                    'UserIdGroupPairs': [
                        {
                            'GroupId': default_sg_id
                        }
                    ]
                }
            ]
        )
        print('--Added Ingress Rule.')

    remove_cidr_rule = default_sg.revoke_egress(
        IpPermissions=[
            {
                'IpProtocol':'-1',
                'IpRanges': [
                    {
                        'CidrIp': '0.0.0.0/0'
                    }
                ]
            }
        ]
    )
    print('--Removed CIDR Egress rule (0.0.0.0/0)')

    # End Add Rules

    # Final Form of New Default Security Group with sub-security groups attached
    describe_default_sg = ec2.describe_security_groups(
        Filters=[
            {
                'Name': 'group-name',
                'Values': [
                    default_sg_name,
                ]
            }
        ]
    )
    print('DESCRIBE ' + default_sg_name + ':\n--' + str(describe_default_sg))
    
    # 3. Attach security group to instance
    all_sg_ids = [sg['GroupId'] for sg in instance.security_groups]   

    if default_sg_id in all_sg_ids:                                         
        print('The Security Group is already in added to the instance.')
    else:
        all_sg_ids.append(default_sg_id)
        instance.modify_attribute(Groups=all_sg_ids)
        new_all_sg_ids = [sg['GroupId'] for sg in instance.security_groups]
        print('ADDED ' + default_sg_name + '(' + default_sg_id + ') to Instance(' + instance.instance_id + ').')
        print('--List of sub-groups: ' + str(new_all_sg_ids))



def create_sg(sg_name,instance_vpc_id):
    create_sg = ec2.create_security_group(
        Description='default security group to allow ingres/egress from same UAIs.',
        GroupName=sg_name,
        VpcId=instance_vpc_id
    )

    sg_id = create_sg['GroupId']

    print('New Security Group: ' + sg_name + ' - ' + sg_id)
    
    sg = ec2_resource.SecurityGroup(sg_id)

    # attach the rules using the UAI's security group ID 
    egress_rule = sg.authorize_egress(
        DryRun=False,
        IpPermissions=[
            {
                'IpProtocol':'-1',
                'UserIdGroupPairs': [
                    {
                        'GroupId': sg_id
                    }
                ]
            }
        ]
    )
    print('--Added Egress rule.')
    ingress_rule = sg.authorize_ingress(
        DryRun=False,
        IpPermissions=[
            {
                'IpProtocol':'-1',
                'IpRanges':[],
                'UserIdGroupPairs': [
                    {
                        'GroupId': sg_id
                    }
                ]
            }
        ]
    )
    print('--Added Ingress Rule.')
    remove_cidr_rule = sg.revoke_egress(
        IpPermissions=[
            {
                'IpProtocol':'-1',
                'IpRanges': [
                    {
                        'CidrIp': '0.0.0.0/0'
                    }
                ]
            }
        ]
    )
    print('--Removed CIDR Egress rule (0.0.0.0/0)')
    return sg_id

def check_common_sg(instance):    
    print('CHECKING for Common Security Group:') 

    all_sg_ids = [sg['GroupId'] for sg in instance.security_groups]
    
    print('Security Groups on instance: ' + str(all_sg_ids))

    common_sg_id = os.environ['common_sg_id']

    if common_sg_id in all_sg_ids:                                         
        print('The Common Security Group is already in attached to the instance. \nDone.')
    else:
        print('The Common Security Group is not attached to instance. Attaching ' + common_sg_id + ' now.')
        all_sg_ids.append(common_sg_id)
        instance.modify_attribute(Groups=all_sg_ids)
        new_all_sg_ids = [sg['GroupId'] for sg in instance.security_groups]
        print('--ADDED Common SG(' + common_sg_id + ') to Instance(' + instance.instance_id + ').')
        print('----List of sub-groups: ' + str(new_all_sg_ids))
        print('------Complete.')
==================================


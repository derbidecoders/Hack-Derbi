# awsutils
import boto3

def checkEc2(conf):

    session = boto3.session.Session(region_name='ap-south-1')
    client = session.client('ec2')

    demo = client.describe_instances(Filters=[{'Name': 'tag:Name', 'Values': ['firstEC2']}])

    # print(demo)
    status = demo['Reservations'][0]['Instances'][0]['State']['Name']

    conf["Status"] = status;
    return conf

def startEc2(conf):

    session = boto3.session.Session(region_name='ap-south-1')
    client = session.client('ec2')

    demo = client.describe_instances(Filters=[{'Name': 'tag:Name', 'Values': ['firstEC2']}])

    # print(demo)
    status = demo['Reservations'][0]['Instances'][0]['State']['Name']

    if status != 'running':
        instance_id = demo['Reservations'][0]['Instances'][0]['InstanceId']
        client.start_instances(InstanceIds=[instance_id])
        conf["Status"] = "Starting"
    else:
        conf["Status"] = status;
    return conf
    

def stopEc2(conf):

    session = boto3.session.Session(region_name='ap-south-1')
    client = session.client('ec2')

    demo = client.describe_instances(Filters=[{'Name': 'tag:Name', 'Values': ['firstEC2']}])

    # print(demo)
    status = demo['Reservations'][0]['Instances'][0]['State']['Name']

    if status != 'stopped':
        instance_id = demo['Reservations'][0]['Instances'][0]['InstanceId']
        client.stop_instances(InstanceIds=[instance_id])
        conf["Status"] = "Stopping"
    else:
        conf["Status"] = status;
    # print(instance_id)
    return conf


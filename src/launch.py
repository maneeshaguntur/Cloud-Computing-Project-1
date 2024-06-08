import boto3
from decouple import config

# Create an EC2 client
ec2_client = boto3.client(
    'ec2',
    region_name='us-east-1',  # Make sure to specify the correct region
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key
)

# Specify the AMI ID
ami_id = "ami-066ea1555baeb8dc4"

# Launch an EC2 instance
response = ec2_client.run_instances(
    ImageId=ami_id,
    MinCount=1,
    MaxCount=1,
    InstanceType="t2.micro",
    TagSpecifications=[
        {
            'ResourceType': 'instance',
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': 'WebTier'
                }
            ]
        }
    ]
)

# Extract the instance ID from the response
instance_id = response['Instances'][0]['InstanceId']

print("Instance ID:", instance_id)

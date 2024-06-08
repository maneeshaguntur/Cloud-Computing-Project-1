import boto3
from decouple import config

# Setup an Amazon EC2 Client
ec2 = boto3.resource(
    'ec2',
    region_name='us-east-1',  # Use the region 'us-east-1'
    aws_access_key_id=config('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=config('AWS_SECRET_ACCESS_KEY')
)

# Launch an EC2 instance
ami_id = "ami-00ddb0e5626798373"  # AMI for Ubuntu 18.04
instance = ec2.create_instances(
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

# Set tags for the EC2 Instance
instance_id = instance[0].id  # Extract the instance ID
ec2.create_tags(
    Resources=[instance_id],
    Tags=[
        {
            'Key': 'Name',
            'Value': 'Your Tag Name'
        }
    ]
)

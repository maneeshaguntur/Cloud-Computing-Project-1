import time
import boto3

REQ_QUEUE = '1225466047-req-queue'
instance_id_list = []
BASE_INSTANCE_ID = 'i-05e1801e030b96f35'
is_0_on = False  

sqs = boto3.client('sqs')
ec2 = boto3.client('ec2')


def start_base_instance():
    global is_0_on
    global instance_id_list
    if not is_0_on:
        done = False
        while done is False:
            try:
                ec2.start_instances(InstanceIds=[BASE_INSTANCE_ID])
                done = True
            except Exception:
                time.sleep(3)

        is_0_on = True


def stop_base_instance():
    global is_0_on
    if is_0_on:
        done = False
        while done is False:
            try:
                ec2.stop_instances(InstanceIds=[BASE_INSTANCE_ID])
                done = True
            except Exception:
                time.sleep(3)

        is_0_on = False


def get_queue_size(queue_url):
    response = sqs.get_queue_attributes(
        QueueUrl=queue_url,
        AttributeNames=['ApproximateNumberOfMessages']
    )
    return int(response['Attributes']['ApproximateNumberOfMessages'])


def launch_instance(count):
    global instance_id_list
    for _ in range(count):  # Use range(count) to iterate 'count' times
        response = ec2.run_instances(
            ImageId='ami-02886a1d75ce4937c',
            InstanceType='t2.micro',
            MaxCount=1,
            MinCount=1,
            TagSpecifications=[
                {
                    'ResourceType': 'instance',
                    'Tags': [
                        {
                            'Key': 'Name',
                            'Value': f'app-tier-instance-{len(instance_id_list)}'
                        }

                    ]
                }
            ])
        instance_ids = [instance['InstanceId'] for instance in response['Instances']]
        instance_id_list.extend(instance_ids)
        print("Launching:", instance_ids)


def terminate_instance(instance_ids):
    ec2.terminate_instances(InstanceIds=instance_ids)
    print("Terminating:", instance_ids)


def main():
    global is_0_on 
    global instance_id_list 
    while True:
        queue_size = get_queue_size(REQ_QUEUE)
        count_instances = len(instance_id_list)
        print("Current instance count:", count_instances)

        if queue_size > count_instances + int(is_0_on):
            # Scale out
            start_base_instance()
            new_count_instances = min(19, queue_size - 1) - count_instances
            launch_instance(new_count_instances)
        elif queue_size == 0 and instance_id_list:
            # Scale in
            time.sleep(1)
            queue_size1 = get_queue_size(REQ_QUEUE)
            if queue_size1 == 0:
                stop_base_instance()
                terminate_instance(instance_id_list)
                instance_id_list = []
        time.sleep(4)


if __name__ == "__main__":
    main()

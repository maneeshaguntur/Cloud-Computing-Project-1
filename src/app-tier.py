import sys
import time
import boto3
import logging
from io import BytesIO
from base64 import b64decode

from model.face_recognition import face_match

ENABLE_S3 = True
S3_INPUT = "1225466047-in-bucket"
S3_OUTPUT = "1225466047-out-bucket"

REQUEST_QUEUE = '1225466047-req-queue'
RESPONSE_QUEUE = '1225466047-resp-queue'
WAIT_TIME = 5
SLEEP_TIME = 3

logging.basicConfig(level=logging.INFO, stream=sys.stdout)

sqs = boto3.resource('sqs')
req_queue = sqs.get_queue_by_name(QueueName=REQUEST_QUEUE)
resp_queue = sqs.get_queue_by_name(QueueName=RESPONSE_QUEUE)


if ENABLE_S3:
    s3 = boto3.client('s3')


def process_message(msg):
    image_data = msg.message_attributes['Image']['StringValue']
    result = face_match(BytesIO(b64decode(image_data)), 'model/data.pt')
    result_data = (msg.body, result[0], image_data)
    return result_data


def send_response_message(filename, result):
    result_attributes = {'StringValue': result, 'DataType': 'String'}
    response = resp_queue.send_message(MessageBody=filename, MessageAttributes={'Result': result_attributes})
    return response


def upload_to_s3(filename, prediction, bucket):
    filename = filename.split('.')[0]
    prediction_bytes = bytes(prediction.encode('utf-8'))
    s3.put_object(Key=filename, Body=prediction_bytes, Bucket=bucket)


if __name__ == "__main__":
    logging.info("Polling req queue....")
    while True:
        time.sle
        messages = req_queue.receive_messages(MessageAttributeNames=['Image'],
                                                  MaxNumberOfMessages=1,
                                                  WaitTimeSeconds=WAIT_TIME)

        if len(messages) == 0:
            logging.info("No messages.")
            time.sleep(SLEEP_TIME)

        start_time = time.time()
        for message in messages:
            filename, prediction, image_data = process_message(message)
            send_response_message(filename, prediction)
            time_taken = round(time.time() - start_time, 2)
            if ENABLE_S3:
                upload_to_s3(filename, prediction, S3_OUTPUT)
                upload_to_s3(filename, image_data, S3_INPUT)
            message.delete()

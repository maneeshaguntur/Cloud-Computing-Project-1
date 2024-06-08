import time
import logging
import boto3
from flask import Flask, request
import base64

app = Flask(__name__)

sqs_client = boto3.client('sqs')
req_queue = '1225466047-req-queue'
resp_queue = '1225466047-resp-queue'
SLEEP_TIME = 3

def send_message_to_req_queue(image):
    req_queue = sqs_client.get_queue_url(QueueName=req_queue)['QueueUrl']
    image_data = base64.b64encode(image.read()).decode("utf-8")
    image_attributes = {'StringValue': image_data, 'DataType': 'String'}
    response = sqs_client.send_message(QueueUrl=req_queue, MessageBody=image.filename, MessageAttributes={'Image': image_attributes})
    return response

def receive_message_from_resp_queue(image):
    resp_queue = sqs_client.get_queue_url(QueueName=resp_queue)['QueueUrl']
    messages = sqs_client.receive_message(QueueUrl=resp_queue, MessageAttributeNames=['Result'],
                                          MaxNumberOfMessages=1, WaitTimeSeconds=3)['Messages']
    if not messages:
        app.logger.info(f"[{image.filename}] No messages in response queue, sleeping for {SLEEP_TIME}s.")
        time.sleep(SLEEP_TIME)
        return None
    else:
        message = messages[0]
        message_attrs = message['MessageAttributes']
        result = message_attrs.get('Result').get('StringValue')
        sqs_client.delete_message(QueueUrl=resp_queue, ReceiptHandle=message['ReceiptHandle'])
        return result

@app.post("/")
def processimage():
    image = request.files['inputFile']
    send_message_to_req_queue(image)
    app.logger.info(f'[{image.filename}] Sent to queue for processing.')

    result = None
    while result is None:
        result = receive_message_from_resp_queue(image)

    return f"{image.filename}:{result}"

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)

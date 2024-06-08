from flask import Flask, request
import boto3

app = Flask(__name__)

# Initialize AWS SQS client
sqs = boto3.client('sqs', region_name='us-east-1')

# URL of your SQS queue
queue_url = 'https://sqs.us-east-1.amazonaws.com/851725196464/1225466047-req-queue'

@app.route('/', methods=['POST'])
def process_images():
    # Check if files were uploaded
    if 'inputFiles' not in request.files:
        return 'No files uploaded', 400

    # Get the uploaded files
    uploaded_files = request.files.getlist('inputFiles')

    # Process each uploaded file
    for file in uploaded_files:
        # Read file content
        file_content = file.read()
        file_content_str = file_content.decode('utf-8')

        # Send file content to SQS queue
        response = sqs.send_message(
            QueueUrl=queue_url,
            MessageBody=file_content_str
        )

        # Check if message was successfully sent
        if response['ResponseMetadata']['HTTPStatusCode'] != 200:
            return 'Error sending message to SQS queue', 500

    return 'Files uploaded and sent to SQS queue successfully'

if __name__ == '__main__':
    app.run(debug=True)

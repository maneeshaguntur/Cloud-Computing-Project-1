import sys
import os
import time
import _thread
import argparse
import requests
import subprocess
import numpy as np
import pandas as pd
import threading
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed

parser = argparse.ArgumentParser(description='Upload images')
parser.add_argument('--num_request', type=int, help='one image per request')
parser.add_argument('--url', type=str, help='URL to the backend server, e.g. http://3.86.108.221/xxxx.php')
parser.add_argument('--image_folder', type=str, help='the path of the folder where images are saved on your local machine')
parser.add_argument('--prediction_file', type=str, help='the path of the classification results file')
args = parser.parse_args()

num_request     = args.num_request
url             = args.url
image_folder    = args.image_folder
prediction_file = args.prediction_file

prediction_df   = pd.read_csv(prediction_file)
responses       = 0
err_responses   = 0
correct_predictions = 0
wrong_predictions   = 0

def send_one_request(image_path):
    global prediction_df, responses, err_responses, correct_predictions, wrong_predictions
    # Define http payload, "myfile" is the key of the http payload
    file = {"inputFile": open(image_path,'rb')}
    response = requests.post(url, files=file)

    # Print error message if failed
    if response.status_code != 200:
        print('sendErr: '+response.url)
        err_responses +=1
    else :
        filename    = image_path.split('/')[-1]
        image_msg   = filename + ' uploaded!'
        msg         = image_msg + '\n' + 'Classification result: ' + response.text
        print(msg)
        responses   +=1
        correct_result = prediction_df.loc[prediction_df['Image'] == filename.split('.')[0], 'Results'].iloc[0]
        if correct_result == response.text.split(':')[1]:
            correct_predictions +=1
        else:
            wrong_predictions +=1

num_max_workers = 100
image_path_list = []
test_start_time = time.time()

for i, name in enumerate(os.listdir(image_folder)):
    if i == num_request:
        break
    image_path_list.append(image_folder + name)

with ThreadPoolExecutor(max_workers = num_max_workers) as executor:
    for r in executor.map(send_one_request, image_path_list):
        if r: print(r)

print ("Waiting ... ")


while True:
    print (".")
    test_duration = time.time() - test_start_time
    if num_request == (responses + err_responses) or test_duration > 300:
        print (f"+++++ Test Result Statistics +++++")
        print (f"Total number of requests: {num_request}")
        print (f"Total number of requests completed successfully: {responses}")
        print (f"Total number of failed requests: {err_responses}")
        print (f"Total number of correct predictions : {correct_predictions}")
        print (f"Total number of wrong predictions: {wrong_predictions}")
        print (f"Total Test Duration: {test_duration} (seconds)")
        print ("++++++++++++++++++++++++++++++++++++")
        break
    time.sleep(1)

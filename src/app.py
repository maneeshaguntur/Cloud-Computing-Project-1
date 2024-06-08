import csv
from flask import Flask, request

app = Flask(__name__)

lookup_data = None
#lookup.csv is Classification Results on Face Dataset (1000 images).csv
with open('lookup.csv', 'r') as csv_file:
    reader = csv.reader(csv_file)
    lookup_data = dict(reader)

@app.post("/")
def perform_lookup():
    input_file = request.files['inputFile']
    
    filename_without_extension = input_file.filename.split('.')[0]
    
    value = lookup_data.get(filename_without_extension, "Value not found")
    
    return f"{input_file.filename}:{value}"

app.run()
    
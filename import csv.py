import csv
import json
import boto3
from io import StringIO

# Initialize the S3 client
s3 = boto3.client('s3')

# Replace with your S3 bucket and file details
bucket_name = 'your-bucket-name'
csv_file_key = 'path/to/your/file.csv'
json_file_key = 'path/to/your/file.json'

# Step 1: Download the CSV file from S3
csv_obj = s3.get_object(Bucket=bucket_name, Key=csv_file_key)
csv_data = csv_obj['Body'].read().decode('utf-8')

# Step 2: Convert CSV to JSON
csv_reader = csv.DictReader(csv_data.splitlines())
rows = list(csv_reader)

# Step 3: Upload JSON back to S3
json_data = json.dumps(rows, indent=4)
json_file = StringIO(json_data)  # StringIO lets us treat the JSON as a file object

# Upload the JSON file to the specified S3 bucket
s3.upload_fileobj(json_file, bucket_name, json_file_key)

print(f"CSV file has been converted to JSON and uploaded to {json_file_key}")

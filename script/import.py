import boto3
import os

# Dell ECS credentials and endpoint from environment variables
DELL_ECS_ACCESS_KEY = os.getenv('S3_ACCESS_KEY_ID')
DELL_ECS_SECRET_KEY = os.getenv('S3_SECRET_ACCESS_KEY')
DELL_ECS_ENDPOINT = os.getenv('S3_ENDPOINT')
BUCKET_NAME = os.getenv('S3_BUCKET')

#DELL_ECS_ENDPOINT = 'https://nrs.objectstore.gov.bc.ca'
#BUCKET_NAME = 'tneelb'  # Replace with your bucket name
#OBJECT_KEY = 'msw_in_region_disposal.csv'  # Replace with the object you want to download
LOCAL_FILE_PATH = './import'  # Local file path for saving the downloaded file

# Initialize the S3 client with Dell ECS endpoint
s3_client = boto3.client('s3', 
                         aws_access_key_id=DELL_ECS_ACCESS_KEY, 
                         aws_secret_access_key=DELL_ECS_SECRET_KEY,
                         endpoint_url=DELL_ECS_ENDPOINT,
                         region_name='us-east-1')  # Adjust region if needed
# List of files to download
files_to_download = [
    'msw_in_region_disposal.xlsx',
    'msw_in_region_disposal.csv',
    'pop_municipal_subprov_areas.xlsx',
]


# Download the file from Dell ECS
for OBJECT_KEY in files_to_download:
    try:
        s3_client.download_file(BUCKET_NAME, OBJECT_KEY, os.path.join(LOCAL_FILE_PATH, OBJECT_KEY))
        print(f"Downloaded {OBJECT_KEY} from Dell ECS to {LOCAL_FILE_PATH}.")
    except Exception as e:
        print(f"Error downloading file: {e}")

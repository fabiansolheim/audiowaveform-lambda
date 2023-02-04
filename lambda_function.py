import json
import boto3
import os
import subprocess

s3 = boto3.client('s3')

def lambda_handler(event, context):
    key = event['s3_key']
    bucket = event['s3_bucket']
    temp_file = "/tmp/file" + key.split('/')[-1]
    
    try:
        s3.download_file(bucket, key, temp_file)
        subprocess.call(['audiowaveform', '-i', temp_file, '--pixels-per-second', '10', '-b', '8', '-o', '/tmp/peaks.json'])
    
        with open('/tmp/peaks.json', 'r') as f:
            file_contents = f.read()
            peaks = json.loads(file_contents)['data']

        os.remove(temp_file)
        os.remove('/tmp/peaks.json')
        
        return {
            'statusCode': 200,
            'body': json.dumps(peaks)
        }
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e

import boto3
import json

BATCH_SIZE = 64
s3 = boto3.resource('s3')

def handler_name(event, context):
    bucket_url = event["body"] # access bucket URL in body
    bucket = s3.Bucket(bucket_url) # define bucket to access
    image_keys = [obj.key for obj in bucket.objects.all()] # get all keys of objects in bucket

    return {
        "statusCode": 200,
        "headers": {"Content-Type:", "application/json"},
        "body": json.dumps({"bucket": bucket_url,
                            "image_keys":image_keys,
                            "batch_size": BATCH_SIZE
                            })
    }

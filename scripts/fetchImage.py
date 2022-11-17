import boto3
import json

def lambda_handler(event, context):
    s3 = boto3.resource('s3')
    bucket_url = event["bucket"] # access bucket URL in body
    batch_size = event["batch_size"]

    bucket = s3.Bucket(bucket_url) # define bucket to access
    image_keys = [obj.key for obj in bucket.objects.all()] # get all keys of objects in bucket

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"bucket": bucket_url,
                            "image_keys":image_keys,
                            "batch_size": batch_size
                            })
    }
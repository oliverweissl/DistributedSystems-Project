import json
import boto3

ACCESS_KEY = None
SECRET_KEY = None
s3 = boto3.resource('s3', aws_access_key_id=ACCESS_KEY,aws_secret_access_key=SECRET_KEY)

def handler_name(event, context):
    bucket_url = event["bucket"]
    image_keys = event["image_keys"]
    batch_size = event["batch_size"]

    bucket = s3.Bucket(bucket_url)  # define bucket to access

    for i in range(0,len(image_keys),batch_size):
        batch_selection = image_keys[i:i+batch_size]
        available_keys = [obj.key for obj in bucket.objects.all()]  # get all keys of objects in bucket
        if batch_selection in available_keys: # if keys not loaded yet
            batch = []
            for key in batch_selection:
                s3.Object(bucket_url, f"loaded/{key}").copy_from(bucket_url, key) # rename keys as loaded
                s3.Object(bucket_url, key).delete() # delete loaded keys
                batch.append(f"loaded/{key}") # add final key to batch
            return {
                "statusCode": 200,
                "headers": {"Content-Type:", "application/json"},
                "body": json.dumps({"bucket": bucket_url, "batch_keys": batch})
            }
        else: raise Exception("Batch not loaded: objects not in Bucket")




import json
import boto3

s3 = boto3.resource("s3")

def handler_name(event, context):
    bucket_url = event["bucket"]
    image_keys = event["image_keys"]
    batch_size = event["batch_size"]

    bucket = s3.Bucket(bucket_url)  # define bucket to access
    available_keys = [obj.key for obj in bucket.objects.all()]  # get all keys of objects in bucket

    for i in range(0,len(available_keys),batch_size):
        batch_selection = image_keys[i:i+batch_size]
        if batch_selection in available_keys: # if keys not loaded yet
            batch = []
            for obj in batch_selection:
                s3.Object(bucket_url, f"loaded/{obj}").copy_from(bucket_url, obj) # rename keys as loaded
                s3.Object(bucket_url, obj).delete() # delete loaded keys
                batch.append(f"loaded/{obj}") # add final key to batch
            return {
                "statusCode": 200,
                "headers": {"Content-Type:", "application/json"},
                "body": json.dumps({"bucket": bucket_url, "batch_keys": batch})
            }
        else: raise Exception("Batch not loaded: objects not in Bucket")




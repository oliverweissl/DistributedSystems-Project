import json
import boto3


def lambda_handler(event, context):
    s3 = boto3.resource('s3')

    bucket_url = event["body"]["bucket"]
    image_keys = event["body"]["image_keys"]
    batch_size = event["body"]["batch_size"]
    emotions = event["body"]["emotions"]
    face_size = event["body"]["face_size"]

    bucket = s3.Bucket(bucket_url)  # define bucket to access
    for i in range(0, len(image_keys), batch_size):
        batch_selection = image_keys[i:i + batch_size]
        available_keys = [obj.key for obj in bucket.objects.all()]  # get all keys of objects in bucket
        if all([item in available_keys for item in batch_selection]):  # if keys not loaded yet
            batch = []
            for key in batch_selection:
                s3.Object(bucket_url, f"loaded/{key}").copy_from(
                    CopySource=f"{bucket_url}/{key}")  # rename keys as loaded
                s3.Object(bucket_url, key).delete()  # delete loaded keys
                batch.append(f"loaded/{key}")  # add final key to batch
            return {
                "statusCode": 200,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({"bucket": bucket_url,
                                    "batch_keys": batch,
                                    "emotions": emotions,
                                    "face_size": face_size})
            }
        else:
            raise Exception("Batch not loaded: objects not in Bucket")
import json
import boto3
from time import perf_counter_ns
from time import time


def lambda_handler(event, context):
    start = time()
    start_perf = perf_counter_ns()
    s3 = boto3.resource('s3')

    json_input = json.loads(event["body"])
    bucket_url = json_input["bucket"]  # access bucket URL in body
    batch_size = json_input["batch_size"]

    bucket = s3.Bucket(bucket_url)  # define bucket to access
    image_keys = [obj.key for obj in bucket.objects.all()]  # get all keys of objects in bucket
    amt = int(len(image_keys)/batch_size+0.5)  # gets amount of sublists --> rounds up to next integer

    stop = perf_counter_ns()
    return {
        "keys": [image_keys[count::amt] for count in range(amt)],
        "start": start,
        "runtime": stop-start_perf
    }
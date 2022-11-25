import io
import json
import math
import boto3
from time import perf_counter_ns
from PIL import Image


def create_collage(image_array: list, sizes: int) -> Image.Image:
    grid_size = math.ceil(math.sqrt(len(image_array)))  # make grid by number of instances
    temp = Image.new("RGB", (sizes * grid_size, sizes * grid_size), "white")  # create blank image for collage

    for i in range(grid_size):
        for j in range(grid_size):
            index = i + j * grid_size  # current index of instance
            if index < len(image_array):
                temp.paste(image_array[index], (i * sizes, j * sizes))  # add face to temp image
    return temp


def lambda_handler(event, context):
    start = perf_counter_ns()

    s3 = boto3.resource('s3')
    client = boto3.client('s3')

    json_input = json.loads(event["body"])
    emotion = json_input["emotion"]
    bucket_url = json_input["bucket"]
    face_size = json_input["face_size"]

    bucket = s3.Bucket(bucket_url)
    images = [Image.open(io.BytesIO(obj.get()['Body'].read())) for obj in bucket.objects.filter(Prefix=f"{emotion}/")]

    if len(images) > 0:
        collage = create_collage(images, face_size)

        in_mem_file = io.BytesIO()
        collage.save(in_mem_file, format="png")
        in_mem_file.seek(0)  # reverses byte-stream to display the image in correct orientation

        client.upload_fileobj(
            in_mem_file,
            bucket_url,
            f"{emotion}_collage.png")

    stop = perf_counter_ns()
    return {
        "start": start,
        "runtime": stop-start,
        "stop": stop
    }

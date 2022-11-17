import io
import sys
import json
import math
import boto3

from pip._internal import main

main(["install", "pillow", "--target", "/tmp/"])
sys.path.insert(0, "/tmp/")
from PIL import Image
import PIL.Image

SIZES = 50


def create_collage(image_array, sizes):
    grid_size = math.ceil(math.sqrt(len(image_array)))
    print(grid_size, len(image_array))
    temp = Image.new("RGB", (sizes * grid_size, sizes * grid_size), "white")
    for i in range(grid_size):
        for j in range(grid_size):
            index = i + j * grid_size
            if index < len(image_array):
                temp.paste(image_array[index], (i * sizes, j * sizes))
    return temp


def bbox_to_arr(bbox):
    return [bbox["Width"], bbox["Height"], bbox["Left"], bbox["Top"]]


def lambda_handler(event, context):
    s3 = boto3.resource('s3')
    client = boto3.client('s3')

    EMOTIONS = event["body"]["emotions"]
    bucket = event["body"]["bucket"]
    detected_faces = event["body"]["detected_faces"]

    keys = []
    bboxe_arr = []
    emotions_arr = []
    for instance in detected_faces:  # look at all detected faces in all images
        keys.append(instance["key"])  # get image key
        bbox = []
        emotions = []
        for face in instance["faces"]:  # for each face in the image
            bbox.append(bbox_to_arr(face["BoundingBox"]))  # extract bounding box
            emotions.append(0 if face["Emotions"]["HAPPY"] > face["Emotions"][
                "SAD"] else 1)  # extract dominat emotion , 0 = Happy, 1 = Sad
        bboxe_arr.append(bbox)
        emotions_arr.append(emotions)

    happy_faces = []
    sad_faces = []
    for i, key in enumerate(keys):  # cutout all faces from each image
        obj = s3.Object(bucket_name=bucket, key=key)
        obj_body = obj.get()['Body'].read()
        img = Image.open(io.BytesIO(obj_body))
        w, h = img.size

        fc = bboxe_arr[i]  # faces in the image
        em = emotions_arr[i]  # emotions for the faces

        for j, face in enumerate(fc):
            width, height, left, top = face[0] * w, face[1] * h, face[2] * w, face[3] * h
            im_crop = img.crop((left, top, left + width, top + height))
            im_crop = im_crop.resize((SIZES, SIZES))
            if em[j] == 0:
                happy_faces.append(im_crop)
            else:
                sad_faces.append(im_crop)

    collections = [happy_faces, sad_faces]
    for i, collection in enumerate(collections):
        if len(collection) > 0:
            collage = create_collage(collection, SIZES)
            in_mem_file = io.BytesIO()
            collage.save(in_mem_file, format="png")
            in_mem_file.seek(0)

            client.upload_fileobj(
                in_mem_file,
                bucket,
                f"{EMOTIONS[i]}_collage.png"
            )

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": "Success!, Check Bucket for Collages."
    }

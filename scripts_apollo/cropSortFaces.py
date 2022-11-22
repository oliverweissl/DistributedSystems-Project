import io
import sys
import json
import boto3

from pip._internal import main
main(["install", "pillow", "--target", "/tmp/"])
sys.path.insert(0, "/tmp/")
from PIL import Image


def get_dominant_emotion(face: dict) -> str:  # extracts key where confidence is highest
    return max(face["Emotions"], key= face["Emotions"].get)


def bbox_to_arr(bbox: dict) -> list:  # returns array with position of bbox
    return [bbox["Width"], bbox["Height"], bbox["Left"], bbox["Top"]]


def lambda_handler(event, context):
    s3 = boto3.resource('s3')
    client = boto3.client('s3')

    json_input = json.loads(event["body"])
    bucket = json_input["bucket"]
    detected_faces = json_input["detected_faces"]
    face_size = json_input["face_size"]

    keys, bbox_arr, emotions_arr = [], [], []
    for instance in detected_faces:  # look at all detected faces in all images
        keys.append(instance["key"])  # get image key

        tmp_bbox_arr, tmp_em_arr = [], []
        for face in instance["faces"]:  # for each face in the image
            tmp_bbox_arr.append(bbox_to_arr(face["BoundingBox"]))  # extract bounding box
            tmp_em_arr.append(get_dominant_emotion(face))  # extract dominant emotion
        bbox_arr.append(tmp_bbox_arr)
        emotions_arr.append(tmp_em_arr)

    for i, key in enumerate(keys):  # cutout all faces from each image
        obj = s3.Object(bucket_name=bucket, key=key)  # get image from S3
        obj_body = obj.get()['Body'].read()  # get image data
        img = Image.open(io.BytesIO(obj_body))  # open image with pillow
        w, h = img.size  # get image dimensions

        tmp_faces = bbox_arr[i]  # faces in the image
        tmp_emotions = emotions_arr[i]  # emotions for the faces

        for j, face in enumerate(tmp_faces):
            width, height, left, top = face[0] * w, face[1] * h, face[2] * w, face[3] * h  # get coordinates of bbox
            im_crop = img.crop((left, top, left + width, top + height))  # crop bbox
            im_crop = im_crop.resize((face_size, face_size))  # standardise size of bbox

            in_mem_file = io.BytesIO()
            im_crop.save(in_mem_file, format="png")
            in_mem_file.seek(0)

            client.upload_fileobj(
                in_mem_file,
                bucket,
                f"{tmp_emotions[j]}_{key.split('.')[0]}_{id(in_mem_file)}.png"
            )

    return {
        "statusCode": 200
    }

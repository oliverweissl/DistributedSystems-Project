import io
import json
import boto3
from time import perf_counter_ns
from time import time
from PIL import Image


def get_dominant_emotion(face: dict) -> str:  # extracts key where confidence is highest
    return max(face["Emotions"], key=face["Emotions"].get)


def bbox_to_list(bbox: dict) -> list:  # returns list with position of bbox
    return [bbox["Width"], bbox["Height"], bbox["Left"], bbox["Top"]]


def lambda_handler(event, context):
    start = time()
    start_perf = perf_counter_ns()

    json_input = json.loads(event["body"])
    bucket_url = json_input["bucket"]
    detected_faces = json_input["detected_faces"]
    face_size = json_input["face_size"]

    s3 = boto3.resource('s3')
    client = boto3.client('s3')

    keys, bbox_arr, emotions_arr = [], [], []
    for instance in detected_faces:  # look at all detected faces in all images
        keys.append(instance["key"])  # get image key

        tmp_bbox_arr, tmp_em_arr = [], []
        for face in instance["faces"]:  # for each face in the image
            tmp_bbox_arr.append(bbox_to_list(face["BoundingBox"]))  # extract bounding box
            tmp_em_arr.append(get_dominant_emotion(face))  # extract dominant emotion

        bbox_arr.append(tmp_bbox_arr)
        emotions_arr.append(tmp_em_arr)

    for i, key in enumerate(keys):  # cutout all faces from each image
        obj = s3.Object(bucket_name=bucket_url, key=key)  # get image from S3
        obj_body = obj.get()['Body'].read()  # get image data

        with Image.open(io.BytesIO(obj_body)) as img:  # open image with pillow
            w, h = img.size  # get image dimensions

            tmp_faces = bbox_arr[i]  # faces in the image
            tmp_emotions = emotions_arr[i]  # emotions for the faces

            for j, face in enumerate(tmp_faces):
                width, height, left, top = face[0] * w, face[1] * h, face[2] * w, face[3] * h  # get coordinates of bbox
                im_crop = img.crop((left, top, left + width, top + height))  # crop bbox
                im_crop = im_crop.resize((face_size, face_size))  # standardise size of bbox

                with io.BytesIO() as in_mem_file:
                    im_crop.save(in_mem_file, format="png")
                    in_mem_file.seek(0)

                    client.upload_fileobj(
                        in_mem_file,
                        bucket_url,
                        f"{tmp_emotions[j]}/{key.split('.')[0]}_{id(in_mem_file)}.png"
                    )

    stop = perf_counter_ns()
    return {
        "start": start,
        "runtime": stop-start_perf
    }

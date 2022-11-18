import io
import sys
import math
import boto3

from pip._internal import main
main(["install", "pillow", "--target", "/tmp/"])
sys.path.insert(0, "/tmp/")
from PIL import Image


def create_collage(image_array: list, sizes: int) -> Image.Image:
    grid_size = math.ceil(math.sqrt(len(image_array)))  # make grid by number of instances
    temp = Image.new("RGB", (sizes * grid_size, sizes * grid_size), "white")  # create blank image for collage

    for i in range(grid_size):
        for j in range(grid_size):
            index = i + j * grid_size  # current index of instance
            temp.paste(image_array[index], (i * sizes, j * sizes))  # add face to temp image
    return temp


def get_dominant_emotion(face: dict) -> str:  # extracts key where confidence is highest
    return max(face["Emotions"], key= face["Emotions"].get)


def bbox_to_arr(bbox: dict) -> list:  # returns array with position of bbox
    return [bbox["Width"], bbox["Height"], bbox["Left"], bbox["Top"]]


def lambda_handler(event, context):
    s3 = boto3.resource('s3')
    client = boto3.client('s3')

    emotions = event["body"]["emotions"]
    bucket = event["body"]["bucket"]
    detected_faces = event["body"]["detected_faces"]
    face_size = event["body"]["face_size"]

    keys, bbox_arr, emotions_arr = [], [], []
    for instance in detected_faces:  # look at all detected faces in all images
        keys.append(instance["key"])  # get image key

        tmp_bbox_arr, tmp_em_arr = [], []
        for face in instance["faces"]:  # for each face in the image
            tmp_bbox_arr.append(bbox_to_arr(face["BoundingBox"]))  # extract bounding box
            tmp_em_arr.append(get_dominant_emotion(face))  # extract dominant emotion
        bbox_arr.append(tmp_bbox_arr)
        emotions_arr.append(tmp_em_arr)

    face_lists = [[None]*len(emotions)]  # create lists for emotions sort
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
            face_lists[emotions.index(tmp_emotions[j])].append(im_crop)  # add image to dedicated sub-list


    for i, collection in enumerate(face_lists):
        if len(collection) > 0:
            collage = create_collage(collection, face_size)
            in_mem_file = io.BytesIO()
            collage.save(in_mem_file, format="png")
            in_mem_file.seek(0)

            client.upload_fileobj(
                in_mem_file,
                bucket,
                f"{emotions[i]}_collage.png"
            )

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": "Success!, Check Bucket for Collages."
    }

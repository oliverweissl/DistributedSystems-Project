import io
import json
import boto3
import asyncio
from time import perf_counter_ns
from time import time
from PIL import Image


async def get_dominant_emotion(face: dict) -> str:  # extracts key where confidence is highest
    return max(face["Emotions"], key=face["Emotions"].get)


async def bbox_to_list(bbox: dict) -> list:  # returns list with position of bbox
    return [bbox["Width"], bbox["Height"], bbox["Left"], bbox["Top"]]


class FaceHandler:
    def __init__(self, event):
        self.json_input = json.loads(event["body"])
        self.bucket_url = self.json_input["bucket"]
        self.detected_faces = self.json_input["detected_faces"]
        self.face_size = self.json_input["face_size"]

        self.s3 = boto3.resource('s3')
        self.client = boto3.client('s3')

        self.keys, self.bbox_arr, self.emotions_arr = [], [], []

    def extract_data(self):
        for instance in self.detected_faces:  # look at all detected faces in all images
            self.keys.append(instance["key"])  # get image key

            tmp_bbox_arr,tmp_em_arr = [], []
            for face in instance["faces"]:
                tmp_bbox_arr.append(bbox_to_list(face["BoundingBox"]))
                tmp_em_arr.append(get_dominant_emotion(face))

            self.bbox_arr.append(asyncio.gather(*tmp_bbox_arr))
            self.emotions_arr.append(asyncio.gather(*tmp_em_arr))

    async def key_handler(self):
        tmp_funct_arr = [self.image_handler(key=key, i=i) for i, key in enumerate(self.keys)]
        await asyncio.gather(*tmp_funct_arr)

    async def image_handler(self, key, i):
        obj = self.s3.Object(bucket_name=self.bucket_url, key=key)
        obj_body = obj.get()['Body'].read()  # get image data

        tmp_faces = self.bbox_arr[i]
        tmp_emotions = self.emotions_arr[i]

        with Image.open(io.BytesIO(obj_body)) as img:
            tmp_funct_arr = [self.crop_save_faces(face=face, j=j, img=img, tmp_emotions=tmp_emotions, key=key)
                             for j, face in enumerate(tmp_faces)]
            await asyncio.gather(*tmp_funct_arr)

    async def crop_save_faces(self, face, j, img, tmp_emotions, key):
        w, h = img.size
        width, height, left, top = face[0] * w, face[1] * h, face[2] * w, face[
            3] * h  # get coordinates of bbox
        im_crop = img.crop((left, top, left + width, top + height))  # crop bbox
        im_crop = im_crop.resize((self.face_size, self.face_size))  # standardise size of bbox

        with io.BytesIO() as in_mem_file:
            im_crop.save(in_mem_file, format="png")
            in_mem_file.seek(0)

            self.client.upload_fileobj(
                in_mem_file,
                self.bucket_url,
                f"{tmp_emotions[j]}/{key.split('.')[0]}_{id(in_mem_file)}.png"
            )


def lambda_handler(event, context):
    start = time()
    start_perf = perf_counter_ns()

    handler = FaceHandler(event)
    handler.extract_data()
    handler.key_handler()

    stop = perf_counter_ns()
    return {
        "start": start,
        "runtime": stop-start_perf
    }

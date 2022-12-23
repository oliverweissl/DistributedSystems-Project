import io
import json
import redis
import base64
from time import perf_counter_ns
from time import time
from PIL import Image


def upload_image(key: str, image: io.BytesIO, c: redis.cluster.RedisCluster):
    base64_enc = base64.b64encode(image.getvalue()).decode("utf-8")
    response = json.dumps({"image": base64_enc})
    c.set(key, response)


def get_image(key: str, c: redis.cluster.RedisCluster) -> io.BytesIO:
    if data := json.loads(c.get(key)):
        image = base64.b64decode(data["image"].encode('utf-8'))
        return io.BytesIO(image)


def get_dominant_emotion(face: dict) -> str:  # extracts key where confidence is highest
    return max(face["Emotions"], key=face["Emotions"].get)


def bbox_to_list(bbox: dict) -> list:  # returns list with position of bbox
    return [bbox["Width"], bbox["Height"], bbox["Left"], bbox["Top"]]


def lambda_handler(event, context):
    start = time()
    start_perf = perf_counter_ns()

    json_input = json.loads(event["body"])
    detected_faces = json_input["detected_faces"]
    face_size = json_input["face_size"]
    redis_ip = json_input["redis"]
    redis_auth = json_input["password"]

    nodes = [redis.cluster.ClusterNode(host=redis_ip, port=7000 + port) for port in range(6)]
    c = redis.cluster.RedisCluster(host=redis_ip, password=redis_auth, port=7000, startup_nodes=nodes)

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
        obj_body = get_image(key, c)

        with Image.open(obj_body) as img:  # open image with pillow
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

                    upload_image(key=f"FACE_{tmp_emotions[j]}_{key.split('.')[0].split('/')[1]}_{j}",
                                 image=in_mem_file,
                                 c=c)

    stop = perf_counter_ns()
    return {
        "start": start,
        "runtime": stop-start_perf
    }

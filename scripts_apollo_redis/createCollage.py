import io
import json
import math
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
    start = time()
    start_perf = perf_counter_ns()

    json_input = json.loads(event["body"])
    emotion = json_input["emotion"]
    face_size = json_input["face_size"]
    redis_ip = json_input["redis"]
    redis_auth = json_input["password"]

    nodes = [redis.cluster.ClusterNode(host=redis_ip, port=7000 + port) for port in range(6)]
    c = redis.cluster.RedisCluster(host=redis_ip, password=redis_auth, port=7000, startup_nodes=nodes)

    images = [Image.open(get_image(key, c))
              for key in [pre_key for pre_key in c.keys(target_nodes=nodes) if emotion in pre_key]]

    if len(images) > 0:
        collage = create_collage(images, face_size)

        in_mem_file = io.BytesIO()
        collage.save(in_mem_file, format="png")
        in_mem_file.seek(0)  # reverses byte-stream to display the image in correct orientation

        upload_image(key=f"COLLAGE_{emotion}", image=in_mem_file, c=c)

    stop_perf = perf_counter_ns()
    stop = time()
    [c.delete(key) for key in c.keys(target_nodes=nodes) if "FACE" in key]
    return {
        "start": start,
        "runtime": stop_perf-start_perf,
        "stop": stop
    }

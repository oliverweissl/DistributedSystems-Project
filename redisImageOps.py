import io
import os
import json
import redis
import base64
from PIL import Image


FILE_DIR = "IMAGES"


def get_image(key: str, c: redis.cluster.RedisCluster):
    if data := c.get(key):
        image = data["image"]
        w, h = data["width"], data["height"]
        Image.frombytes(image, w, h).save(f"{key}.jpg", format="jpg")


def upload_image(dir: str, c: redis.cluster.RedisCluster):
    key, fmt = dir.split("/")[-1].split(".")
    in_mem_file = io.BytesIO()
    img = Image.open(dir)
    w, h = img.size()
    img.save(in_mem_file, format=fmt)
    base64_enc = base64.b64decode(in_mem_file.seek(0).read())

    response = json.dumps({
        "image": base64_enc,
        "width": w,
        "height": h
    })
    c.set(key, response)


host_ip = input("Enter Host: ")
password_str = input("Enter Password: ")

c = redis.cluster.RedisCluster(host=host_ip, password=password_str, port=7000)
value_pairs = c.scan_iter(target_nodes=c.ALL_NODES)


images = [f"{FILE_DIR}/{file}" for file in os.listdir(FILE_DIR)]
print(images)
print(value_pairs)
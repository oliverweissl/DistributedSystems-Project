import io
import json
import redis
import base64
from PIL import Image


FILE_DIR = "IMAGES"

HOST = "44.203.194.143"
PW = "testpw"


def get_image(key: str, c):
    if data := json.loads(c.get(key)):
        image = base64.b64decode(data["image"].encode('utf-8'))
        Image.open(io.BytesIO(image)).save(f"{key}.jpg")


def upload_image(dir: str, c):
    key, *_ = dir.split("/")[-1].split(".")

    in_mem_file = io.BytesIO()
    img = Image.open(dir)
    img.save(in_mem_file, format="jpeg")
    base64_enc = base64.b64encode(in_mem_file.getvalue()).decode("utf-8")

    response = json.dumps({"image": base64_enc})
    c.set(key, response)


#host_ip = input("Enter Host: ")
#password_str = input("Enter Password: ")

c = redis.Redis(host=HOST, password=PW)
#c = redis.cluster.RedisCluster(host=host_ip, password= password_str, port=7000)


"""
#upload images
images = [f"{FILE_DIR}/{file}" for file in os.listdir(FILE_DIR)]
for image in images:
    upload_image(dir=image, c=c)


#download images
value_pairs = c.scan_iter()
keys = c.keys()
for val, key in zip(value_pairs, keys):
    get_image(key= key, c=c)
"""
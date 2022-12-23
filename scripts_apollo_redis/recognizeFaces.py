import json
import boto3
import redis
import base64
import io
from time import perf_counter_ns
from time import time


def get_image(key: str, c: redis.cluster.RedisCluster) -> io.BytesIO:
    if data := json.loads(c.get(key)):
        image = base64.b64decode(data["image"].encode('utf-8'))
        return io.BytesIO(image)


class RekognitionImage:
    def __init__(self, key: str, c: redis.cluster.RedisCluster, rekognition_client: boto3.client, emotions: list):
        self.rekognition_client = rekognition_client
        self.c = c
        self.key = key
        self.image = get_image(self.key, self.c)
        self.emotions = emotions

    def extract_emotions(self, emotions_dict: dict) -> dict:
        r_dict = {}
        for val in self.emotions:  # reduce dict to {Emotion: ConfidenceValue}
            r_dict.update({val: [entry for i, entry in enumerate(emotions_dict)
                                 if emotions_dict[i]["Type"] == val][0]["Confidence"]})
        return r_dict

    def detect_faces(self) -> list:
        response = self.rekognition_client.detect_faces(
            Image={self.image},
            Attributes=['ALL'])

        faces = [{"BoundingBox": face["BoundingBox"],
                  "Confidence": face["Confidence"],
                  "Emotions": self.extract_emotions(face["Emotions"])} for face in response["FaceDetails"]]
        return faces


def lambda_handler(event, context):
    start = time()
    start_perf = perf_counter_ns()

    json_input = json.loads(event["body"])
    images = json_input["split_keys"]
    emotions = json_input["emotions"]
    redis_ip = json_input["redis"]
    redis_auth = json_input["password"]

    nodes = [redis.cluster.ClusterNode(host=redis_ip, port=7000 + port) for port in range(6)]
    c = redis.cluster.RedisCluster(host=redis_ip, password=redis_auth, port=7000, startup_nodes=nodes)
    rekognition_client = boto3.client('rekognition')

    all_faces = []
    for key in images:
        detected_faces = RekognitionImage(key, c,rekognition_client, emotions).detect_faces()
        all_faces.append({
            "key": key,
            "faces": detected_faces})

    stop = perf_counter_ns()
    return {
        "detected_faces": all_faces,
        "start": start,
        "runtime": stop-start_perf
    }

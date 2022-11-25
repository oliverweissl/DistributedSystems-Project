import json
import boto3
from time import perf_counter_ns

class RekognitionImage:
    def __init__(self, key: str, bucket: str, emotions: list):
        self.rekognition_client = boto3.client('rekognition')
        self.bucket = bucket
        self.key = key
        self.emotions = emotions

    def extract_emotions(self, emotions_dict: dict) -> dict:
        r_dict = {}
        for val in self.emotions:  # reduce dict to {Emotion: ConfidenceValue}
            r_dict.update({val: [entry for i, entry in enumerate(emotions_dict)
                                 if emotions_dict[i]["Type"] == val][0]["Confidence"]})
        return r_dict

    def detect_faces(self) -> list:
        response = self.rekognition_client.detect_faces(
            Image={'S3Object': {'Bucket': self.bucket, 'Name': self.key}},
            Attributes=['ALL'])

        faces = [{"BoundingBox": face["BoundingBox"],
                  "Confidence": face["Confidence"],
                  "Emotions": self.extract_emotions(face["Emotions"])} for face in response["FaceDetails"]]
        return faces


def lambda_handler(event, context):
    start = perf_counter_ns()

    json_input = json.loads(event["body"])
    images = json_input["split_keys"]
    bucket_url = json_input["bucket"]
    emotions = json_input["emotions"]

    all_faces = []
    for key in images:
        detected_faces = RekognitionImage(key, bucket_url, emotions).detect_faces()
        all_faces.append({
            "key": key,
            "faces": detected_faces})

    stop = perf_counter_ns()
    return {
        "detected_faces": all_faces,
        "start": start,
        "runtime": stop - start
    }

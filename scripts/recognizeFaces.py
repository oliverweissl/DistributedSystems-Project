import json
import io
import boto3
from botocore.exceptions import ClientError

EMOTIONS = ["HAPPY", "SAD"]

def extract_emotions(emotions_dict):
    selected = emotions_dict[0:2]
    return {EMOTIONS[0]: selected[0]["Confidence"],
            EMOTIONS[1]: selected[1]["Confidence"]}

class RekognitionImage:
    def __init__(self, key, bucket, rekognition_client):
        self.rekognition_client = rekognition_client
        self.bucket = bucket
        self.key = key

    def detect_faces(self):
        response = self.rekognition_client.detect_faces(
            Image={'S3Object': {'Bucket': self.bucket, 'Name': self.key}},
            Attributes=['ALL'])

        faces = [{"BoundingBox": face["BoundingBox"],
                  "Confidence": face["Confidence"],
                  "Emotions": extract_emotions(face["Emotions"])} for face in response["FaceDetails"]]
        return faces


def lambda_handler(event, context):
    rekognition = boto3.client('rekognition')

    bucket = event["body"]["bucket"]
    images = event["body"]["batch_keys"]

    faces = []
    for key in images:
        detected_faces = RekognitionImage(key, bucket, rekognition).detect_faces()
        faces.append({
            "key": key,
            "faces": detected_faces})

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({
            "bucket": bucket,
            "emotions": EMOTIONS,
            "detected_faces": faces
        })
    }

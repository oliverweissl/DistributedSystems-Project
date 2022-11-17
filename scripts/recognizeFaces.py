import json
import io
import boto3
from botocore.exceptions import ClientError

ATTRIBUTES = ["BoundingBox", "Confidence", "Emotions"]


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
                  "Emotions": face["Emotions"]} for face in response["FaceDetails"]]
        return faces


def lambda_handler(event, context):
    rekognition = boto3.client('rekognition')
    s3 = boto3.resource('s3')

    bucket = event["body"]["bucket"]
    images = event["body"]["batch_keys"]

    faces = {}
    for key in images:
        detected_faces = RekognitionImage(key, bucket, rekognition).detect_faces()
        if detected_faces is not None:
            faces.update({key: detected_faces})

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({
            "bucket": bucket,
            "detected_faces": faces
        })
    }

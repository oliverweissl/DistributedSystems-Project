import json
import boto3


def extract_emotions(emotions_dict: dict, emotions: list) -> dict:
    r_dict = {}
    for val in emotions: # reduce dict to {Emotion: ConfidenceValue}
        r_dict.update({val: [entry for entry in emotions_dict if emotions_dict[entry]["Type"] == val][0]["Confidence"]})
    return r_dict


class RekognitionImage:
    def __init__(self, key, bucket, rekognition_client, emotions: list):
        self.rekognition_client = rekognition_client
        self.bucket = bucket
        self.key = key
        self.emotions = emotions

    def detect_faces(self) -> list:
        response = self.rekognition_client.detect_faces(
            Image={'S3Object': {'Bucket': self.bucket, 'Name': self.key}},
            Attributes=['ALL'])

        faces = [{"BoundingBox": face["BoundingBox"],
                  "Confidence": face["Confidence"],
                  "Emotions": extract_emotions(face["Emotions"], self.emotions)} for face in response["FaceDetails"]]
        return faces


def lambda_handler(event, context):
    rekognition = boto3.client('rekognition')

    bucket = event["bucket"]
    images = event["split_keys"]
    emotions = event["emotions"]

    faces = []
    for key in images:
        detected_faces = RekognitionImage(key, bucket, rekognition, emotions).detect_faces()
        faces.append({
            "key": key,
            "faces": detected_faces})

    return {
        "detected_faces": json.dumps(faces)
    }

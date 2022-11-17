import json
import boto3
from botocore.exceptions import ClientError

ACCESS_KEY = None
SECRET_KEY = None
rekognition = boto3.client('rekognition', aws_access_key_id=ACCESS_KEY,aws_secret_access_key=SECRET_KEY)

class RekognitionImage:
    def __init__(self, key, bucket, rekognition_client):
        self.image = s3.Object(bucket, key)["Body"] # probably worng
        self.rekognition_client = rekognition_client

    def detect_faces(self):
        try:
            response = self.rekognition_client.detect_faces(
                Image=self.image, Attributes=['BoundingBox','Confidence','Emotions'])
            faces = [face for face in response['FaceDetails']]
            print("Detected %s faces.", len(faces))
        except ClientError:
            raise Exception("Couldn't detect faces in %s.", self.image_name)
        else:
            return faces




def handler_name(event, context):
    bucket = event["bucket"]
    images = event["batch_keys"]

    faces = dict
    for key in images:
        detected_faces = RekognitionImage(key, bucket, rekognition).detect_faces()
        faces.update({key: detected_faces})


    return {
        "statusCode": 200,
        "headers": {"Content-Type:", "application/json"},
        "body": json.dumps({
            "bucket": bucket,
            "detected_faces": faces
        })
    }

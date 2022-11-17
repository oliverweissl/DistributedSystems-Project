import json


def lambda_handler(event, context):
    var = event["body"]

    # Do something

    return {
        "statusCode": 200,
        "headers": {"Content-Type:", "application/json"},
        "body": json.dumps(var)
    }

import json


def handler_name(event, context):
    var = event["body"]

    # Do something

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(var)
    }

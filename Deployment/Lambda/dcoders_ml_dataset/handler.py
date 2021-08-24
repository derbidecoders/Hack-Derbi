try:
    import unzip_requirements
except importError:
    pass
import os
import io
import json
import base64
from requests_toolbelt.multipart import decoder
import requests

from ModelStatus import ModelStatus

def infer_model(event, context):
    # try:
    content_type_header = event['headers']['content-type']
    body = base64.b64decode(event["body"])
    if type(event["body"]) is str:
        event["body"] = bytes(event["body"], "utf-8")

    multipart_data = decoder.MultipartDecoder(body, content_type_header)

    requestJson = json.loads(multipart_data.parts[0].content)
    # print(requestJson)
    if( requestJson["State"] == "IMG_TEST"):
        picture = decoder.MultipartDecoder(body, content_type_header).parts[1]
        requestJson["img"] = base64.b64encode(picture.content).decode("utf-8")
        result = requests.post("https://speech.rohitrnath.xyz/imginfer", json=requestJson, verify=False)
        result = result.json()

    elif( requestJson["State"] == "IMG_TEST_MULTI"):
        picture = decoder.MultipartDecoder(body, content_type_header).parts[1]
        requestJson["img"] = base64.b64encode(picture.content).decode("utf-8")
        result = requests.post("https://speech.rohitrnath.xyz/chestxray", json=requestJson, verify=False)
        #result = result.json()

    elif( requestJson["State"] == "INFER_MODEL"):
        result = ModelStatus( requestJson)

    response = result
    return {
        "statusCode": 200,
        "headers": {
            'content-type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Credentials': True

        },
        "body": json.dumps(response)
    }
    # except Exception as e:
    #     print(repr(e))
    #     return {
    #         'statusCode': 500,
    #         "headers": {
    #             'content-type': 'application/json',
    #             'Access-Control-Allow-Origin': '*',
    #             "Access-Control-Allow-Credentials": True
    #         },
    #         "body": json.dumps({"error": repr(e)})
    #     }
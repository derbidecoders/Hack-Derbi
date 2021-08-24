try:
    import unzip_requirements
except ImportError:
    pass

import boto3
import os
import io
import json
import base64
import copy
# import numpy as np
from operator import itemgetter

from requests_toolbelt.multipart import decoder

from genToken import genToken
from ImageRecoUpload import ImageRecoUpload
from CSVRecoUpload import CSVRecoUpload
from awsutils import startEc2, stopEc2, checkEc2


headers = {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Credentials": True,
}

def enigmaManager(event, context):

    try:
        content_type_header = event['headers']['content-type']
        # print(event['body'])
        body = base64.b64decode(event["body"])
        if type(event["body"]) is str:
            event["body"] = bytes(event["body"], "utf-8")

        multipart_data = decoder.MultipartDecoder(body, content_type_header)

        requestJson = json.loads(multipart_data.parts[0].content)
        # print(requestJson)
        if( requestJson["State"] == "IMG_UPLOAD"):
            picture = decoder.MultipartDecoder(body, content_type_header).parts[1]
            result = ImageRecoUpload( requestJson, image_bytes=picture.content)
        elif( requestJson["State"] == "CSV_UPLOAD"):
            csvfile = decoder.MultipartDecoder(body, content_type_header).parts[1]
            result = CSVRecoUpload( requestJson, csv_bytes=csvfile.content)
        elif( requestJson["State"] == "GEN_TOKEN"):
            result = genToken(requestJson)
        elif( requestJson["State"] == "EC2_ON" ):
            result = startEc2(requestJson)
        elif( requestJson["State"] == "EC2_OFF" ):
            result = stopEc2(requestJson)
        elif( requestJson["State"] == "EC2_CHECK" ):
            result = checkEc2(requestJson)
            
        response = result
        return {"statusCode": 200, "headers": headers, "body": json.dumps(response)}

    except ValueError as ve:
        # logger.exception(ve)
        print(ve)
        return {
            "statusCode": 422,
            "headers": headers,
            "body": json.dumps({"error": repr(ve)}),
        }
    except Exception as e:
        # logger.exception(e)
        print(e)
        return {
            "statusCode": 500,
            "headers": headers,
            "body": json.dumps({"error": repr(e)}),
        }


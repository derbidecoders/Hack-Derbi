import os
import base64
import torch
import torchvision
import torchvision.transforms as transforms
import io
import PIL
from PIL import Image
import json

from s3utils import download_file, getByteStream

S3_BUCKET = "capstone-eva"
def transform_image(image_bytes):

    try:
        imagenet_stats = ([0.5270, 0.5794, 0.6113], [0.1725, 0.1665, 0.1815])
        transformations = transforms.Compose([
            transforms.Resize((224,224), interpolation=PIL.Image.BICUBIC),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(*imagenet_stats)])
        image = Image.open(io.BytesIO(image_bytes))
        return transformations(image).unsqueeze(0)
    except Exception as e:
        print(repr(e))
        raise(e)

def get_prediction( model, image_bytes):
    tensor = transform_image(image_bytes=image_bytes)
    return model(tensor).argmax().item()



def ImageInfer( conf):
    b64_bytes = conf["img"].encode('utf-8')
    image_bytes = base64.decodebytes(b64_bytes)
    result = {}
    recordFile    = conf["TOKEN_ID"]+"/output.json"
    records = getByteStream( S3_BUCKET, recordFile)
    print(records)
    if records:
        InfoJson = json.load(records)
        if (InfoJson["Project"] == "IMG_REC"):
            if(InfoJson["State"] == "MODEL_READY"):
                print(1)
                print(conf["TOKEN_ID"])
                path = getByteStream("capstone-eva", conf["TOKEN_ID"]+"/model.pt")
                model = torch.jit.load(path)
                prediction = get_prediction( model, image_bytes)
                result["State"] = InfoJson["State"]
                result["prediction"] = InfoJson["classes"][prediction]
#                os.remove(path)
            else:
                result["State"] = "Error"
                result["Msg"]	= "Still training in progress!"
        else:
            result["State"] = "Error"
            result["Msg"]	= "Access token is not for image classsification!"
    else:
        result["State"] = "Error"
        result["Msg"]	= "Access token not found!"

    return result

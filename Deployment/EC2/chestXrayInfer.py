import os
import base64
import numpy as np
import matplotlib.pyplot as plt
import torch
import torchvision
import torchvision.transforms as transforms
import json
import io
import copy
import PIL
from PIL import Image
import cv2
import json

from chestXrayNet import chestXrayNet
from gradcam import *
from s3utils import download_file, getByteStream

S3_BUCKET = "capstone-eva"

pathology_list = ['No Findings','Pneumothorax','Pneumonia','Edema','Effusion','Emphysema']

nihdata_stats = ([0.485,0.456,0.406], [0.229,0.224,0.225])

def transform_image(image_bytes):

    try:
        transformations = transforms.Compose([
            transforms.Resize((224,224)),
            transforms.ToTensor(),
            transforms.Normalize(*nihdata_stats)])
        image = Image.open(io.BytesIO(image_bytes))
        return transformations(image)
    except Exception as e:
        print(repr(e))
        raise(e)



def deprocess(img):
    img = img.permute(1,2,0)
    img = img * torch.Tensor(nihdata_stats[0]) + torch.Tensor(nihdata_stats[1])
    return img

def view_classify(img, ps, heatmap=None):

    class_name = pathology_list
    classes = np.array(class_name)

    ps = ps.cpu().data.numpy().squeeze()
    img = deprocess(img)
    #img = np.transpose(img, (1, 2, 0))[:,:,0]
    # class_labels = list(np.where(label==1)[0])

    # if not class_labels :
    #     title = 'No Findings'
    # else : 
    #     title = itemgetter(*class_labels)(class_name)
        


    fig, (ax1, ax2, ax3) = plt.subplots(figsize=(12,3), ncols=3)
    ax1.imshow(img)
    ax1.set_title('Input Image')
    ax1.axis('off')
    # if(heatmap != None):
    ax2.imshow(img)
    ax2.imshow(heatmap, alpha=0.25, cmap='jet')
    ax2.set_title('Gradcam')
    ax2.axis('off')

    ax3.barh(classes, ps)
    ax3.set_aspect(0.1)
    ax3.set_yticks(classes)
    ax3.set_yticklabels(classes)
    ax3.set_title('Predicted Class')
    ax3.set_xlim(0, 1.1)

    plt.tight_layout()
    with io.BytesIO() as buff:
        plt.savefig(buff, format='raw')
        buff.seek(0)
        data = np.frombuffer(buff.getvalue(), dtype=np.uint8)
    w, h = fig.canvas.get_width_height()
    im = data.reshape((int(h), int(w), -1))
    # plt.savefig('rohit.png')

    return im

def get_prediction( model, image_bytes):
    tensor = transform_image(image_bytes=image_bytes)
    with torch.no_grad():
        ps = model(tensor.unsqueeze(0))
        modelCPU = copy.deepcopy(model.network)
    target_layer = modelCPU.features.norm5
    gradcam = GradCAM(modelCPU, target_layer)
    cam, heatmap, pred = gradcam.forward(image.unsqueeze(0), retain_graph=True)
    img = view_classify( tensor, ps, heatmap)
    return img


def ChestXrayInfer( conf):
    b64_bytes = conf["img"].encode('utf-8')
    image_bytes = base64.decodebytes(b64_bytes)
    result = {}
    recordFile    = conf["TOKEN_ID"]+"/output.json"
    records = getByteStream( S3_BUCKET, recordFile)
    print(records)
    if records:
        InfoJson = json.load(records)
        if (InfoJson["Project"] == "IMG_REC_MULTI"):
            if(InfoJson["State"] == "MODEL_READY"):
                print(1)
                print(conf["TOKEN_ID"])
                path = getByteStream("capstone-eva", conf["TOKEN_ID"]+"/model.pth")
                #model = torch.jit.load(path)
                model = chestXrayNet()
                model.load_state_dict(torch.load(path))
                image_p = get_prediction( model, image_bytes)
                output_img = Image.fromarray(cv2.cvtColor(image_p, cv2.COLOR_RGB2BGR))
                result["State"] = InfoJson["State"]
                result["output"] = base64.b64encode(output_img).decode("utf-8")
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

    return json.dumps(result)

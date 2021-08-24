from flask import Flask
import threading
from flask import jsonify
from flask import request
import os
import json
from s3utils import *
from imageRecognision import imageRecognision
from nlpClassification import nlpClassification
from imageInfer import ImageInfer
from NLPInfer import NLPInfer
from chestXrayInfer import ChestXrayInfer

app = Flask(__name__)

from flask_cors import CORS
cors = CORS(app, resources={r"/imgrecog/*": {"origins": "*"}})
cors2 = CORS(app, resources={r"/hello/*": {"origins": "*"}})
cors3 = CORS(app, resources={r"/nlpclassify/*": {"origins": "*"}})
cors4 = CORS(app, resources={r"/nlpinfer/*": {"origins": "*"}})

@app.route('/hello', methods=['POST'])
def hello():
   param = request.get_json()
   return jsonify({'status' : True})


@app.route('/imginfer', methods=['POST'])
def imgInfer():
  params = request.get_json()
  response = ImageInfer(params)
  print(response)
  return response

@app.route('/chestxray', methods=['POST'])
def chestXInfer():
  params = request.get_json()
  response = ChestXrayInfer(params)
  print(response)
  return response

@app.route('/nlpinfer', methods=['POST'])
def nlpInfer():
  params = request.get_json()
  response = NLPInfer(params)
  print(response)
  return response

@app.route('/imgrecog', methods=['POST'])
def imgRecog():
    params = request.get_json()
    print(params)
    ID = params["TOKEN_ID"]
    epochs = int(params["Epochs"])
    Ratio = int(params["Ratio"])
    downloadDirectoryFroms3( 'capstone-eva', ID)
    f = open(ID+"/userInfo.json",)
    info = json.load(f)
    f.close()
    if (info["Project"]=="IMG_REC") and (info["TOKEN_ID"]==params["TOKEN_ID"]):
      #thread = threading.Thread(target=imageRecognision,
#                                      args=(ID, epochs, Ratio, ), daemon=True)
      #thread.start()
      imageRecognision(ID, epochs, Ratio)
      return jsonify({'status' : True})
    else:
      return jsonify({'status' : False})

@app.route('/nlpclassify', methods=['POST'])
def NLPclassify():
    params = request.get_json()
    print(params)
    ID = params["TOKEN_ID"]
    epochs = int(params["Epochs"])
    Ratio = int(params["Ratio"])
    downloadDirectoryFroms3( 'capstone-eva', ID)
    f = open(ID+"/userInfo.json",)
    info = json.load(f)
    f.close()
    if (info["Project"]=="NLP_CLS") and (info["TOKEN_ID"]==params["TOKEN_ID"]):
      nlpClassification(ID, epochs, Ratio)
      return jsonify({'status' : True})
    else:
      return jsonify({'status' : False})

if __name__ == "__main__":
    app.run(host='0.0.0.0')

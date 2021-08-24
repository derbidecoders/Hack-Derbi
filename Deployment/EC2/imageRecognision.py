import os
import shutil
import PIL
import torchvision.transforms as T
import torch
import json

from s3utils import *
from model import MobilenetV2
from dataloader import *
from train import fit_one_cycle, evaluate

import boto3

def remove(path):
    """ param <path> could either be relative or absolute. """
    if os.path.isfile(path) or os.path.islink(path):
        os.remove(path)  # remove the file
    elif os.path.isdir(path):
        shutil.rmtree(path)  # remove dir and all contains
    else:
        raise ValueError("file {} is not a file or dir.".format(path))

def imageRecognision(moduleName, epochs=5, Ratio=80, batch_size = 5, max_lr = 0.01, grad_clip=0.1, weight_decay=1e-4, opt_func = torch.optim.SGD ):
  # downloadDirectoryFroms3( 'capstone-eva', moduleName)
  
  BASEDIR = moduleName + '/dataset'

  imagenet_stats = ([0.5270, 0.5794, 0.6113], [0.1725, 0.1665, 0.1815])

  train_tfms = T.Compose([
      T.Resize( (224,224), interpolation=PIL.Image.BICUBIC), 
      T.RandomCrop(224, padding=8, padding_mode='reflect'),
      # T.RandomResizedCrop(224, scale=(0.5,0.9), ratio=(1, 1)), 
      # T.ColorJitter(brightness=0.1, contrast=0.1, saturation=0.1, hue=0.1),
      T.RandomHorizontalFlip(),
      # T.RandomVerticalFlip(),
      T.RandomRotation((-30,+30)), 
      T.ToTensor(),
      T.Normalize(*imagenet_stats,inplace=True), 
      T.RandomErasing(inplace=True)
  ])

  valid_tfms = T.Compose([
      T.Resize( (224,224), interpolation=PIL.Image.BICUBIC),
      T.ToTensor(),
      T.Normalize(*imagenet_stats)
  ])

  random_seed = 42
  torch.manual_seed(random_seed);
  data, train_dl, test_dl = dataloader( BASEDIR, train_transform=train_tfms, valid_transform=valid_tfms, Ratio=Ratio, batch_size= 15, shuffle = True)

  dict =  {}
  dict["Project"]="IMG_REC"
  dict["State"] = "START_TRAIN"
  dict["ID"] = moduleName
  dict["classes"] = data.classes
  dict["Ratio"] = Ratio
  dict["totalEpochs"] = epochs
  dict["epoch"] = 0

  
  with open(moduleName+"/output.json", "w") as outfile:
    json.dump(dict, outfile)
  upload_file("output.json",'capstone-eva', moduleName+"/")


  device = get_default_device()
  train_dl = DeviceDataLoader(train_dl, device)
  val_dl = DeviceDataLoader(test_dl, device)
  model_local = MobilenetV2(len(data.classes))
  model  = to_device(model_local, device);

  history = [evaluate(model, val_dl)]
  model.freeze()

  history += fit_one_cycle(epochs, max_lr, model, train_dl, val_dl, 
                         grad_clip=grad_clip, 
                         weight_decay=weight_decay, 
                         opt_func=opt_func)
  
#  model.unfreeze()

#  history += fit_one_cycle(epochs, 0.005, model, train_dl, val_dl, 
#                         grad_clip=grad_clip, 
#                         weight_decay=1e-5, 
#                         opt_func=opt_func)
  

  traced_model = torch.jit.trace(model.cpu(),torch.randn(1,3,224,224))
  traced_model.save(moduleName+'/model.pt')
  upload_file('model.pt','capstone-eva', moduleName+"/")

  dict["history"] = history;
  dict["State"] = "MODEL_READY"
  with open(moduleName+"/output.json", "w") as outfile:
    json.dump(dict, outfile)
  upload_file("output.json",'capstone-eva', moduleName+"/")

  remove(moduleName)

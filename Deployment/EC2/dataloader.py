import numpy as np
from torchvision.datasets import ImageFolder
from torchvision.transforms import ToTensor
from torch.utils.data.dataloader import DataLoader
from torch.utils.data import Subset
import torchvision.transforms as T
import torch


def dataloader( path, train_transform=T.ToTensor(), valid_transform=T.ToTensor(), Ratio=80, batch_size=64, shuffle=False):
  
  traindataset = ImageFolder( path, transform=train_transform)
  valdataset = ImageFolder( path, transform=valid_transform)

  train_size = Ratio/100
  num_train = len(traindataset)
  indices = list(range(num_train))
  split = int(np.floor(train_size * num_train))
  np.random.shuffle(indices)
  train_idx, valid_idx = indices[:split], indices[split:]

  traindata = Subset(traindataset, indices=train_idx)
  valdata = Subset(valdataset, indices=valid_idx)
  # train_size = int(0.8 * len(dataset))
  # test_size = len(dataset) - train_size
  # train_dataset, test_dataset = torch.utils.data.random_split(dataset, [train_size, test_size])
  # train_dataset = train_dataset.map(train_transform)
  # test_dataset  = test_dataset.map(valid_transform)
  train_dl = DataLoader(traindata, batch_size, shuffle=shuffle)
  test_dl = DataLoader(valdata, batch_size, shuffle=None)

  return traindataset, train_dl, test_dl

def get_default_device():
    """Pick GPU if available, else CPU"""
    if torch.cuda.is_available():
        return torch.device('cuda')
    else:
        return torch.device('cpu')
    
def to_device(data, device):
    """Move tensor(s) to chosen device"""
    if isinstance(data, (list,tuple)):
        return [to_device(x, device) for x in data]
    return data.to(device, non_blocking=True)

class DeviceDataLoader():
    """Wrap a dataloader to move data to a device"""
    def __init__(self, dl, device):
        self.dl = dl
        self.device = device
        
    def __iter__(self):
        """Yield a batch of data after moving it to device"""
        for b in self.dl: 
            yield to_device(b, self.device)

    def __len__(self):
        """Number of batches"""
        return len(self.dl)
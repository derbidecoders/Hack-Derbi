*#EZ-MedMod AI (A.K.A. Dcoders AI)*
***The Dcoders AI is a No-Code AI platform which automates the training and deployment of deep learning applications.***

*To access the DCoders AI webapp, [click here](https://rohitrnath.s3.ap-south-1.amazonaws.com/DCoders/index.html)*

## The webapp has two functions.

* **Patients/Users Assist:** Deployed the multi-disease diagnosis using 
  Chest X-ray images model here. Here the users can upload the images and validate the model accuracy with *Explainable AI* visualisation(GradCAM).

* **Researchers Assist:** This is a proof-of-concept of our product EZ-MedMod.
  Currently we implemented an image classification template, which ingests images with their class labels and spits out a model that can classify those images and any new images given to it.

  

### The tech stack uses following services

* AWS EC2: to train the model
* AWS Lambda: to process the API Requests, model inference and to invoke EC2
* AWS S3: to store dataset, model and config files
* PyTorch: to train models

### The folder contents

* UI:UX: the source code used for front-end development
* EC2: to train the model
* Lambda:
  * dcoders_service_dataset : To process the API request, update S3 DB and to invoke the EC2
  * dcoders_dl_service : To model inference

## Code Files

* ***Dcoders_Final_Densenet121.ipynb***
  This is the major training notebook, which is used to train the dataset on pre-trained densenet151 model and analyse its performance.
  We experimented with three basic deep learning models (ResNet18, ResNet50, DenseNet121) at first, and decided to use DenseNet121 as a baseline model. We evaluated our approach and achieved better results, whose average F1 score is 0.7406 and average ROC score is 0.8755, under the NIH Chest X-Ray dataset and its patient-wise split. We proposed an entropy weighting loss to observe inter-label dependencies and make full use of class whose cases are fewer than others.
* ***Resnet50_training.ipynb***
  The file is used to train the dataset on resnet50 model and study its performance. It shows the loss graph after training for various epochs and the weights are stored for inferencing. 
* ***DataSplit_70Train_20Validation_10Test.ipynb***
  This file is used to fetch the CSV database file and patient-wise split it into train, validation and test in 70:20:10 ratio. This file also contains some data analysis of the dataset.
* ***DataSetMerging.ipynb*** 
  This file is used to merge various datasets in to single zip file. It reads the data from various dataset files, resize into 224x224, convert into PNG format and merge to form single file. It also update the CSV file with image name and its class. 



## 
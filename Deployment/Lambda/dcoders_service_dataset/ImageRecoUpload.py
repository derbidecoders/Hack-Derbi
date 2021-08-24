from s3utils import IsFileAvailable, upload_file
import json
import io
import os
from PIL import Image

S3_BUCKET   =   os.environ['S3_BUCKET'] 

def ImageRecoUpload( conf, image_bytes):
	img = Image.open(io.BytesIO(image_bytes))
	img = img.convert('RGB')
	img.save("/tmp/"+ str(conf["Fname"]) + ".jpg")
	try:
		response = upload_file(str(conf["Fname"]) + ".jpg", S3_BUCKET, conf["TOKEN_ID"]+"/dataset/"+conf["Label"]+"/")
	except ClientError as e:
		conf["Status"] = False
		conf["ERROR"] = e
		return conf
	conf["Status"] = True
	os.remove("/tmp/"+ str(conf["Fname"]) + ".jpg")
	return conf
	
try:
    import unzip_requirements
except importError:
    pass
import os
import json

from s3utils import IsFileAvailable, getByteStream


S3_BUCKET   =   os.environ['S3_BUCKET'] 

def ModelStatus(conf):
	result = {}
	recordFile    = conf["TOKEN_ID"]+"/output.json"
	records = getByteStream( S3_BUCKET, recordFile)
	if records:
		InfoJson = json.load(records)
		result["State"] = InfoJson["State"]
		result["Project"] = InfoJson["Project"]
	else:
		result["State"] = "Error"
		result["Msg"]	= "Access token not found!"
	
	return result
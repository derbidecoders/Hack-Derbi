from random import randint
from s3utils import IsFileAvailable, upload_file
import json
import os

NUM_PAD = 3
S3_BUCKET   =   os.environ['S3_BUCKET'] 

def genToken(conf):
	tokenID = 0
	while(1):
		digit = "".join(["{}".format(randint(0, 9)) for num in range(0, NUM_PAD)])
		tokenID = conf["Name"].lower() + digit
		tokenFound = IsFileAvailable( S3_BUCKET, tokenID)
		if(not tokenFound):
			break
	conf["TOKEN_ID"] = tokenID

	with open("/tmp/userInfo.json", "w") as outfile:
		json.dump(conf, outfile)
	
	upload_file("userInfo.json", S3_BUCKET, tokenID+"/")

	return conf



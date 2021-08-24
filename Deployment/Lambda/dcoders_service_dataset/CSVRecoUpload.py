from s3utils import IsFileAvailable, upload_file
import json
import io
import os
import pandas as pd

S3_BUCKET   =   os.environ['S3_BUCKET'] 

def CSVRecoUpload(conf, csv_bytes):
	filename   = "/tmp/data.csv"
	with open(filename, 'wb') as f:
		f.write(csv_bytes)
	df = pd.read_csv(filename)
	num_rows = df.shape[0]
	if(num_rows < 100):
		conf["Status"] = "Error"
		conf["Msg"] = f"Atleast 100 text samples. CSV file contains only '{num_rows} samples'!"
		return conf
	if(num_rows > 1000):
		conf["Status"] = "Error"
		conf["Msg"] = f"This project supports atmost 1000 text samples required. CSV file contains '{num_rows} samples'!"
		return conf
	input_cols = list(df.columns.values)
	if "messages" not in input_cols:
		conf["Status"] = "Error"
		conf["Msg"] =  '"messages" column is missing in CSV file. Please mention the input text column as "messages"'
		return conf

	if "labels" not in input_cols:
		conf["Status"] = "Error"
		conf["Msg"] =  '"labels" column is missing in CSV file. Please mention the label/class name column as "labels"'
		return conf

	labelCount = df['labels'].nunique()
	if  labelCount > 3:
		conf["Status"] = "Error"
		conf["Msg"] =  f'CSV containd {labelCount} unique labels. As of now this project supports maximum 3 labels.'
		return conf

	if  labelCount < 2:
		conf["Status"] = "Error"
		conf["Msg"] =  f'CSV containd {labelCount} labels. Atleast 2 unique labels required to continue.'
		return conf

	try:
		response = upload_file("data.csv", S3_BUCKET, conf["TOKEN_ID"]+"/dataset/")
	except ClientError as e:
		conf["Status"] = "up_error"
		conf["Msg"] = "File upload failed!"
		conf["ERROR"] = e
		return conf
	os.remove(filename)


	conf["Status"] = "Success"
	conf["Msg"]  = "CSV file is verified and uploaded successfully!"
	conf["Stat"] = f'Number of Rows : {num_rows}, Label Count : {labelCount}'

	return conf


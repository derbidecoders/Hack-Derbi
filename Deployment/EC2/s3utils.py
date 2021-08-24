import boto3
import os
import io

def upload_file(file_name, bucket, path):
    """
    Function to upload a file to an S3 bucket
    """
    object_name = file_name
    s3_client = boto3.client('s3', aws_access_key_id= 'AKIA3YOQLOD6CEOIWH7O',
                  aws_secret_access_key= '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')
    response = s3_client.upload_file(path+file_name, bucket, path + object_name)

    return response

def download_file(file_name, bucket):
     """
     Function to download a given file from an S3 bucket
     """
     s3 = boto3.resource('s3', aws_access_key_id= 'AKIA3YOQLOD6CEOIWH7O',
                   aws_secret_access_key= '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')
     output = f"downloads/{file_name}"
     s3.Bucket(bucket).download_file(file_name, file_name)

     return output

def IsFileAvailable(bucketName, remoteFileName):

    fileStatus = False
    s3_resource = boto3.resource('s3', aws_access_key_id= 'AKIA3YOQLOD6CEOIWH7O',
                  aws_secret_access_key= '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')
    bucket = s3_resource.Bucket(bucketName)
    for obj in bucket.objects.filter(Prefix = remoteFileName):
        fileStatus = True
    return fileStatus

def getByteStream(bucketName, remoteFileName):
    #try:
        if IsFileAvailable( bucketName, remoteFileName):
            s3 = boto3.client('s3', aws_access_key_id= 'AKIA3YOQLOD6CEOIWH7O',
                  aws_secret_access_key= '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')
            obj = s3.get_object(Bucket=bucketName, Key=remoteFileName)
            bytestream = io.BytesIO(obj['Body'].read())

            return bytestream
        else:

            return False
    #except Exception as e:

     #   print("Error")
      #  return False

#def download_file(modulename,file_name, bucket):
#    """
#    Function to download a given file from an S3 bucket
#    """
#    s3 = boto3.resource('s3', aws_access_key_id= 'AKIA3YOQLOD6CEOIWH7O',
#                  aws_secret_access_key= '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')
#    output = f"{modulename}/{file_name}"
#    filekey = modulename+"/"+file_name
#    s3.Object(bucket, output).download_file(output)
#    return output

def downloadDirectoryFroms3(bucketName, remoteDirectoryName):
    s3_resource = boto3.resource('s3', aws_access_key_id= 'AKIA3YOQLOD6CEOIWH7O',
                  aws_secret_access_key= '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')
    bucket = s3_resource.Bucket(bucketName)
    for obj in bucket.objects.filter(Prefix = remoteDirectoryName):
        if not os.path.exists(os.path.dirname(obj.key)):
            os.makedirs(os.path.dirname(obj.key))
        bucket.download_file(obj.key, obj.key) # save to same path

def list_files(bucket):
    """
    Function to list files in a given S3 bucket
    """
    s3 = boto3.client('s3', aws_access_key_id= 'AKIA3YOQLOD6CEOIWH7O',
                  aws_secret_access_key= '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')
    contents = []
    for item in s3.list_objects(Bucket=bucket)['Contents']:
        contents.append(item)

    return contents

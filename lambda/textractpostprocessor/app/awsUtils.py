import boto3
import json
import pandas as pd

_s3Client = None

def getS3Client():
    global _s3Client
    if( _s3Client is None):
        _s3Client = boto3.client('s3')
    return _s3Client

def readTextFileFromS3( bucketName, prefix ):
    s3Client = getS3Client()
    print( "reading from bucket ", bucketName, " key ", prefix)
    data = s3Client.get_object(Bucket=bucketName, Key=prefix)
    contents = data['Body'].read()
    return contents.decode("utf-8")

def split_s3_path(s3_path):
    path_parts = s3_path.replace("s3://","").split("/")
    bucket = path_parts.pop(0)
    key = "/".join(path_parts)
    return bucket, key

def readJSONFileFromS3( bucketName, prefix ):
    s3Client = getS3Client()
    print( "reading from bucket ", bucketName, " key ", prefix)
    data = s3Client.get_object(Bucket=bucketName, Key=prefix)
    contents = data['Body'].read()
    return contents.decode("utf-8")

def getExtractedDataFromS3( bucketName, prefix ):
    contents = readTextFileFromS3(bucketName,prefix)
    json_content = json.loads(contents)
    data = pd.DataFrame(json_content["Blocks"])
    dataFiltered = pd.DataFrame(data[data.BlockType.eq('LINE')])
    #if 'Confidence' in dataFiltered.columns:
    #    dataFiltered = dataFiltered[dataFiltered['Confidence']> 80]
    return dataFiltered

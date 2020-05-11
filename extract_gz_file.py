# python imports
import boto3, json
from io import BytesIO
import gzip

# setup constants
# bucket = 'noelcomprehendbucket'
# gzipped_key = 'output-4.tar'
# uncompressed_key = 'my_ouput'

try:
     s3 = boto3.resource('s3')
     key='output.tar.gz'
     obj = s3.Object('noelcomprehendbucket',key)
     n = obj.get()['Body'].read()
     gzipfile = BytesIO(n)
     gzipfile = gzip.GzipFile(fileobj=gzipfile)
     content = gzipfile.read()
     print(content)
except Exception as e:
    print(e)
    raise e
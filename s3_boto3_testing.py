import boto3, pprint

s3 = boto3.resource('s3')

noelbeerbucket = s3.Bucket('noelbeerbucket')

# for m in dir(noelbeerbucket):
# 	print(m)

print(dir(noelbeerbucket.objects))

for item in noelbeerbucket.objects.all():
	print(item)
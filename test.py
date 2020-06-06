import boto3, time, os, re
from pprint import pprint

def start_job(s3_bucket_name, object_name):
	response = None
	client = boto3.client('textract')
	response = client.start_document_text_detection(
		DocumentLocation = {
			'S3Object': {
				'Bucket': s3_bucket_name,
				'Name': object_name
			}
		})
	return response['JobId']

def is_job_complete(job_id):
	#time.sleep(5)
	client = boto3.client('textract')
	response = client.get_document_text_detection(JobId=job_id)
	status = response["JobStatus"]
	print("Job status: {}".format(status))

	while status == "IN_PROGRESS":
		time.sleep(5)
		response = client.get_document_text_detection(JobId=job_id)
		status = response["JobStatus"]
		print("Job status: {}".format(status))

	return status


def get_job_results(job_id):
	pages = []
	client = boto3.client('textract')
	response = client.get_document_text_detection(JobId=job_id)

	pages.append(response)
	print("Number of responses received: {}".format(len(pages)))
	next_token = None
	if 'NextToken' in response:
		next_token = response['NextToken']

	while next_token:
		#time.sleep(5)
		response = client.get_document_text_detection(JobId=job_id, NextToken = next_token)

		pages.append(response)
		print("Number of responses received: {}".format(len(pages)))
		next_token = None
		if 'NextToken' in response:
			next_token = response['NextToken']
	return pages

def get_s3_files(bucket):
	my_s3_files = []
	s3_resource = boto3.resource('s3')
	my_bucket = s3_resource.Bucket(bucket)

	for s3_file in my_bucket.objects.all():
		my_s3_files.append(s3_file)

	return my_s3_files #list

s3_client = boto3.client('s3')

########
# Document
s3_bucket_name = 'noelbeerbucket'
s3_output_bucket = 'noeltextractedbucket'
#beer_bucket_files = get_s3_files(s3_bucket_name)

input_s3_uri = "s3://noeltextractedbucket"
output_s3_uri = "s3://noelcomprehendbucket"
data_access_role_arn = 'arn:aws:iam::332292479439:role/allow_comprehend'

#pprint.pprint(beer_bucket_files)

folder_regex = re.compile(r'.*/')

beer_bucket_files = get_s3_files(s3_bucket_name)
bucket_items = []
for item in beer_bucket_files:
	bucket_items.append(item.key)

# Files with suffix: new_folder/ etc.
nested_bucket_items = list(filter(folder_regex.match, bucket_items))

# print(nested_bucket_items)
all_files = []
for item in beer_bucket_files:
	if item.key in nested_bucket_items:
		all_files.append(folder_regex.sub('', item.key))
	else:
		all_files.append(item.key)

# pprint(bucket_items)
# pprint(all_files)

for item in bucket_items:
	try:
		job_id = start_job(s3_bucket_name, item)
		print("Started TEXTRACT job with id {}".format(job_id))
		if is_job_complete(job_id):
			response = get_job_results(job_id)

		# iterate through all_files list if bucket_files titles work
		
		if item in nested_bucket_items:
			item = folder_regex.sub('', item)
		file_name = '{}.txt'.format(item)
		with open(file_name, 'w') as f:
			for job_result in response:			
				if 'Blocks' not in job_result:
					continue
				else:					
					for item in job_result['Blocks']:
						if item['BlockType'] == 'LINE':
							f.write(item['Text'] + '\n')
				s3_client.upload_file(file_name, s3_output_bucket, file_name)
			# os.remove(file_name)
	except FileNotFoundError as error:
		print(error)
		print('There was an error')

	#print(title)

# import text_to_topic

# job_id = text_to_topic.start_job(input_s3_uri, output_s3_uri, data_access_role_arn)
# print("Started COMPREHEND job with id: {}".format(job_id))
# if text_to_topic.is_job_complete(job_id):
# 	response = text_to_topic.get_job_results(job_id)
# 	pprint.pprint(response)


######################

# # Iterates through S3 bucket PDFs to extract text and save text to textfile. -SUCCESS!!
# for item in beer_bucket_files:
# 	try:
# 		job_id = start_job(s3_bucket_name, item.key)
# 		print("Started TEXTRACT job with id {}".format(job_id))
# 		if is_job_complete(job_id):
# 			response = get_job_results(job_id)
# 			#print(response)

# 		file_name = '{}.txt'.format(item.key)
# 		with open(file_name, 'w') as f:
# 			for job_result in response:
# 				if 'Blocks' not in job_result:
# 					continue
# 				else:					
# 					for item in job_result['Blocks']:
# 						if item['BlockType'] == 'LINE':
# 							f.write(item['Text'] + '\n')
# 				s3_client.upload_file(file_name, s3_output_bucket, file_name)
# 			os.remove(file_name)
# 	except KeyError as error:
# 		print(error)
# 		print('There was an error')
# 	# upload_to_s3(s3_bucket_name, file_name)
# # Iterates through S3 bucket PDFs to extract text and save text to textfile. -SUCCESS!!

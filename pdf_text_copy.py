import boto3, time, pprint

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
beer_bucket_files = get_s3_files(s3_bucket_name)

input_s3_uri = "s3://noeltextractedbucket"
output_s3_uri = "s3://noelcomprehendbucket"
data_access_role_arn = 'arn:aws:iam::332292479439:role/allow_comprehend'


#pprint.pprint(beer_bucket_files)

# Iterates through S3 bucket PDFs to extract text and save text to textfile. -SUCCESS!!
for item in beer_bucket_files:
#	if item.key.endswith('.pdf'):
	try:
		job_id = start_job(s3_bucket_name, item.key)
		print("Started TEXTRACT job with id {}".format(job_id))
		if is_job_complete(job_id):
			response = get_job_results(job_id)
			#print(response)
			
			# for i in range(1, len(beer_bucket_files)+1):
			# file_name = 'my_file_{}.txt'.format(beer_bucket_files.index(item)+1)
		
			for job_result in response:
				if 'Blocks' not in job_result:
					continue
				else:
					file_name = '{}.txt'.format(item.key)
					with open(file_name, 'w') as f:
						for item in job_result['Blocks']:
							if item['BlockType'] == 'LINE':
								f.write(item['Text'] + '\n')
					s3_client.upload_file(file_name, s3_output_bucket, file_name)
	except KeyError as error:
		print(error)
		print('There was an error')
	# upload_to_s3(s3_bucket_name, file_name)
# Iterates through S3 bucket PDFs to extract text and save text to textfile. -SUCCESS!!

import text_key_phrases

job_id = text_key_phrases.start_job(input_s3_uri, output_s3_uri, data_access_role_arn)
print("Started COMPREHEND job with id: {}".format(job_id))
if text_key_phrases.is_job_complete(job_id):
	response = text_key_phrases.get_job_results(job_id)
	pprint.pprint(response)




#print(get_s3_files(s3_bucket_name)[-1].key)
# document_name = '2019 | John,K | Earthworms offset straw-induced increase of greenhouse gas emission in upland rice production.pdf'

# job_id = start_job(s3_bucket_name, document_name)
# print("Started job with id {}".format(job_id))

# if is_job_complete(job_id):
# 	response = get_job_results(job_id)

# #print(response)

# # Write text to a file
# with open('my_file3.txt', 'w') as f:
# 	for result_page in response:
# 		for item in result_page["Blocks"]:
# 			if item["BlockType"] == "LINE":
# 				f.write(item["Text"] + '\n')

# text = ""
# for result_page in response:
# 		for item in result_page["Blocks"]:
# 			if item["BlockType"] == "LINE":
# 				text += item["Text"] + '\n'

# with open('text_result.txt', 'w') as f:
# 	f.write(text)

# comprehend_client = boto3.client('comprehend')
# entities = comprehend_client.detect_entities(LanguageCode='en', Text=text)

# with open('my_entities.txt', 'w') as f:
# 	#f.write("\nEntities\n=============")
# 	for entity in entities["Entities"]:
# 		f.write("{}\t=>\t{}".format(entity["Type"], entity["Text"]))


# comprehend_client = boto3.client('comprehend')
# key_phrases = comprehend_client.detect_key_phrases(Text=text, LanguageCode='en')

# with open('my_key_phrases.txt', 'w') as f:
# 	#f.write("\nEntities\n=============")
# 	for key_phrase in key_phrases["KeyPhrases"]:
# 		f.write(key_phrase["Text"])
















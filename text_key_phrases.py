import boto3, time, pprint

def start_job(input_s3_uri, output_s3_uri, data_access_role_arn):
	response = None
	client = boto3.client('comprehend')
	response = client.start_key_phrases_detection_job(
		InputDataConfig={
        'S3Uri': input_s3_uri,
        'InputFormat': 'ONE_DOC_PER_FILE'# 'ONE_DOC_PER_LINE' #'ONE_DOC_PER_FILE'
    }, OutputDataConfig={
        'S3Uri': output_s3_uri
    }, DataAccessRoleArn=data_access_role_arn,
    LanguageCode = 'en')

	return response["JobId"]

def is_job_complete(job_id):
	#time.sleep(5)
	client = boto3.client('comprehend')
	response = client.describe_key_phrases_detection_job(JobId=job_id)
	status = response['KeyPhrasesDetectionJobProperties']["JobStatus"]
	print("Job status: {}".format(status))

	while status != "COMPLETED":
		time.sleep(5)
		response = client.describe_key_phrases_detection_job(JobId=job_id)
		status = response['KeyPhrasesDetectionJobProperties']["JobStatus"]
		print("Job status: {}".format(status))		

	return status

def get_job_results(job_id):
	pages = []
	client = boto3.client('comprehend')
	response = client.describe_key_phrases_detection_job(JobId=job_id)

	pages.append(response)
	print("Number of responses received: {}".format(len(pages)))


	return pages




# Documents
# input_s3_uri = "s3://noeltextractedbucket"
# output_s3_uri = "s3://noelcomprehendbucket"
# data_access_role_arn = 'arn:aws:iam::332292479439:role/allow_comprehend'

# job_id = start_job(input_s3_uri, output_s3_uri, data_access_role_arn)
# print("Started COMPREHEND job with id: {}".format(job_id))
# if is_job_complete(job_id):
# 	response = get_job_results(job_id)
# 	pprint.pprint(response)

# arn:aws:s3:::noelbeerbucket
import boto3
from botocore.exceptions import ClientError


class storess3:

	def __init__(self):
		self.S3 = boto3.resource('s3', 
			region_name='us-east-2',
    		aws_access_key_id='AKIAJTOEI7DQ3EDG7IZQ',
    		aws_secret_access_key='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')

		# self.data1 = data1
		# self.data2 = data2

	def upload_data_to_s3(self, data, key_name, bucketName):

		try:

			self.S3.Bucket(bucketName).upload_file(data, key_name)
			print ("File %s is uploaded successfully" %(key_name))
		except ClientError as e:
			print ("Something is not working %s" %(e))

	def download_data_from_s3(self, keyname, download_location, bucketName):

		try:
			self.S3.Bucket(bucketName).download_file(keyname, download_location)
			print ("File %s downloaded succesfully" %(keyname))
		except ClientError as e:
			print ("Something is  not working %s" %(e))


S3_obj = storess3()
S3_obj.upload_data_to_s3('/Users/bimleshsharma/Desktop/Screenshot-2.png','Screenshot-4.png','tests3action-bim')
S3_obj.download_data_from_s3('Screenshot-4.png','/Users/bimleshsharma/Desktop/DN_Screenshot-4.png','tests3action-bim')



import boto3
from botocore.exceptions import ClientError


class storess3:

	def __init__(self):
		self.S3 = boto3.resource('s3') 
			
		# self.data1 = data1
		# self.data2 = data2

	def list_all_buckets(self):
		print ( "Here are list of bucket...")
		buckets = [bucket.name for bucket in self.S3.buckets.all()]
		print (buckets)
		return buckets

	def finding_bucket(self, bucket_name):
		if bucket_name in self.list_all_buckets():
			print (" This bucket is already exists...")
			return True
		else:
			print (" This bucket is does not exists...")
			return False

	def delete_bucket(self, bucket_name):
		
		if self.finding_bucket(bucket_name):
			try:
				self.S3.Bucket(bucket_name).delete()
				print ("Bucket %s deleted successfully" %bucket_name)
			except ClientError as E:
				print ("Not able to delete bucket %s" %E)

		
	def create_s3_bucket(self, bucket_name):
		print ("Creating s3 bucket...")
		try:
			self.S3.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={'LocationConstraint':'us-west-1'})
			print ("Bucket %s created successfully" %bucket_name)
		except ClientError as E:
			print ("Something wrong in creating bucket %s" %E)

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

	def select_option(self, option):
		switcher = {
			1 : "List Buckets",
			2 : "Create Buckets"
			}
		print (switcher)



if __name__ == "__main__":

	S3_obj = storess3()
	S3_obj.select_option(2)

	# S3_obj.upload_data_to_s3('/Users/bimleshsharma/Desktop/Screenshot-2.png','Screenshot-4.png','tests3action-bim')
	# S3_obj.download_data_from_s3('Screenshot-4.png','/Users/bimleshsharma/Desktop/DN_Screenshot-4.png','tests3action-bim')
	# S3_obj.list_all_buckets()
	# S3_obj.create_s3_bucket("bim-auto-bucket")
	# S3_obj.finding_bucket("tests3action-bim")
	# S3_obj.delete_bucket("bim-auto-bucket")



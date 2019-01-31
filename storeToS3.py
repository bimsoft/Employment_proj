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
			files = self.list_all_files_from_bucket(bucket_name)
			try:
				if len(files) == 0:
					self.S3.Bucket(bucket_name).delete()
					print ("Bucket %s deleted successfully" %bucket_name)
				else:
					print ("This bucket has files... Deleting file first...wait...")
					self.delete_files_from_bucket(bucket_name, files)
					print ("Now deleting Bucket %s" %bucket_name)
					self.S3.Bucket(bucket_name).delete()

			except ClientError as E:
				print ("Not able to delete bucket %s" %E)
		else:
			print ("COuld not find Bucket %s" %bucket_name)

		
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

	def list_all_files_from_bucket(self, bucket_name):
		bucketname = self.S3.Bucket(bucket_name)
		files = [file.key.encode('ascii', 'ignore') for file in bucketname.objects.all()]
		return files

	def delete_files_from_bucket(self, bucket_name, *file_names):
		if isinstance(file_names, tuple):
			file_names = file_names[0]	
		for file_name in file_names:
			if file_name in self.list_all_files_from_bucket(bucket_name):
				self.S3.Object(bucket_name,file_name).delete()
				print ("Files from bucket has been deleted...")
			else:
				print ("File %s is not available in %s bucket" %(file_name,bucket_name))
		
	
	def select_option(self, option):
		switcher = {
			1 : "List Buckets",
			2 : "Create Buckets"
			}
		print (switcher)



if __name__ == "__main__":

	S3_obj = storess3()
	choices = '''
					1 for Listing bucket
					2 for Create New bucket
					3 for finding bucket
					4 for Deleteing bucket
					5 for upload file into bucket
					6 for download file into bucket
					7 for list out all files of bucket
					8 for delete file(s) from bucket
					9 for make bucket empty

				  '''
	# S3_obj.create_s3_bucket('bim-auto-bucket')
	S3_obj.upload_data_to_s3('/Users/bimleshsharma/Desktop/Screenshot-2.png','Screenshot-4.png','bim-auto-bucket')
	S3_obj.list_all_files_from_bucket('bim-auto-bucket')
	# S3_obj.delete_files_from_bucket('bim-auto-bucket','Screenshot-1.png','Screenshot-2.png')	
	S3_obj.delete_bucket('bim-auto-bucket')

	while False:
		print (choices)
		selection = int(input ("Enter your choice -: "))
		if selection == 0:
			break

		if selection == 1:
			S3_obj.list_all_buckets()
		if selection == 2:
			S3_obj.create_s3_bucket("bim-auto-bucket")
		if selection == 3:
			S3_obj.finding_bucket("tests3action-bim")
		if selection == 4:
			S3_obj.delete_bucket("bim-auto-bucket")
		if selection == 5:
			S3_obj.upload_data_to_s3('/Users/bimleshsharma/Desktop/Screenshot-2.png','Screenshot-4.png','tests3action-bim')
		if selection == 6:
			S3_obj.download_data_from_s3('Screenshot-4.png','/Users/bimleshsharma/Desktop/DN_Screenshot-4.png','tests3action-bim')
		if selection == 7:
			S3_obj.download_data_from_s3('Screenshot-4.png','/Users/bimleshsharma/Desktop/DN_Screenshot-4.png','tests3action-bim')
		if selection == 8:
			S3_obj.list_all_files_from_bucket('bim-auto-bucket')
		if selection == 8:
			S3_obj.delete_files_from_bucket('bim-auto-bucket','Screenshot-7.png')
		
			
	
	



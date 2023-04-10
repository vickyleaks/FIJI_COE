from minio import Minio
from dotenv import load_dotenv
from difflib import SequenceMatcher
import os
load_dotenv()
print("start")
# files = "D:\TWC\Test POs for OCR BOT\erewhon\EREWHON PO2257.pdf" 
# ACCESS_KEY = "wonderful"
# SECRET_KEY = "wo@$nd2rerf#ul341"
# MINIO_API_HOST = "server.singularitysystems.com:5003" 
# bucket_name = "singuimg-7008"
# folder_path = "D:\Robot\FIJI_COE\Singularity Data\Outputs\\"
# minio_foldername = 'class-17-invoice-output-passed'

def upload_files_into_minio(bucket_name,minio_foldername,files,ACCESS_KEY,SECRET_KEY,minio_api_host): 
   try:
      MINIO_CLIENT = Minio(minio_api_host, access_key=ACCESS_KEY, secret_key=SECRET_KEY, secure=True)
      found = MINIO_CLIENT.bucket_exists(bucket_name)

      if not found:
         MINIO_CLIENT.make_bucket(bucket_name) 
      else:
         print("Bucket already exists") 

      list_file = files.split(",") 
      for eachfile in list_file:
         MINIO_CLIENT.fput_object(bucket_name, '/'+ minio_foldername +'/'+ eachfile.split("\\")[-1],eachfile,)
         print(eachfile + ': is uploaded')  
      print("It is successfully uploaded to bucket") 
      return "Succesfully uploaded the files" 
   except Exception as e:
      return "Failed at uploading file: " + str(e) 
# print(upload_files_into_minio(bucket_name,minio_foldername,files,ACCESS_KEY,SECRET_KEY,MINIO_API_HOST)) 


def download_files_from_minio(bucket_name,minio_foldername,folder_path,ACCESS_KEY,SECRET_KEY,minio_api_host):
   try:
      MINIO_CLIENT = Minio(minio_api_host, access_key=ACCESS_KEY, secret_key=SECRET_KEY, secure=True)
      print('start') 
      for objects in MINIO_CLIENT.list_objects(bucket_name,prefix="/"+minio_foldername+"/"): 
         if '.placeholder' in objects.object_name:
            print('placeholder') 
         else:
            filename = objects.object_name.split('/')[1]
            # fileextension = os.path.splitext(filename)[1]  
            # filename = os.path.splitext(filename)[0] 
            # filename = filename + '.comGREATERTHAN' + fileextension
            # MINIO_CLIENT.fget_object(bucket_name,objects.object_name,folder_path +'/' + objects.object_name.split('/')[1])
            MINIO_CLIENT.fget_object(bucket_name,objects.object_name,folder_path +'/' + filename)
            print(objects.object_name + ': file is downloaded') 
            # return objects.object_name.split('/')[-1]
            return filename 
            break
         # MINIO_CLIENT.remove_object(bucket_name, objects.object_name)
      return "No files in " + minio_foldername + ' folder'
   except Exception as e:
      return "Failed at downloading file: " + str(e) 

# print(download_files_from_minio(bucket_name,minio_foldername,folder_path,ACCESS_KEY,SECRET_KEY,MINIO_API_HOST)) 

def delete_files_from_minio(bucket_name,minio_foldername,delete_files,ACCESS_KEY,SECRET_KEY,minio_api_host):
   try:
      MINIO_CLIENT = Minio(minio_api_host, access_key=ACCESS_KEY, secret_key=SECRET_KEY, secure=True)
      # delete_files = delete_files.replace('.comGREATERTHAN','') 
      MINIO_CLIENT.remove_object(bucket_name,minio_foldername+'/' +delete_files)
      return 'The given file was deleted: '+ delete_files
      # objects_to_delete = MINIO_CLIENT.list_objects(bucket_name, prefix=minio_foldername, recursive=True)
      # for obj in objects_to_delete:
      #    if obj.object_name == 'Testing/4511163664.pdf':
      #       MINIO_CLIENT.remove_object(bucket_name, obj.object_name) 
      #       print('delete file: ' + obj.object_name) 
      #    print(obj.object_name) 
   except Exception as e:
      print('Deletion file was failed: '+str(e))  
      return 'Deletion file was failed: '+str(e) 
# delete_files_from_minio(bucket_name,minio_foldername,files,ACCESS_KEY,SECRET_KEY,MINIO_API_HOST)


def address_match(address1, address2, match_ratio):
	match_word = address1
	words = address2
	match_ratio = match_ratio
	max_ratio = 0
	match_got = ""
	try:
		ratio = SequenceMatcher(None,match_word.lower(),words.lower()).ratio() * 100
		print(ratio)
		if ratio > int(match_ratio):
			max_ratio = ratio
			match_got = words
			return True
		else :
			return False
	except Exception as e:
		print("cannnot find match")
		print(e)
		return False 
# print(address_match('Ross Brothers', 'rOss br._ther5','50')) 
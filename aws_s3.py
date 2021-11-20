# -*- coding: utf-8 -*-
"""
Created on Mon Sep 20 15:50:32 2021

@author: ameya
"""
import PIL
from PIL import Image
import boto3
import requests
import keys_config as keys
import urllib.request


def flipping_image(url):
    url_name = url.split('/')[-1].split('.')[0]
    urllib.request.urlretrieve(url, url_name+".jpg")
    
    im = Image.open(url_name+".jpg")
    out = im.transpose(PIL.Image.FLIP_LEFT_RIGHT)
    out.save(url_name+'_transformed.jpg')
    
    return out
    

def upload_file_to_aws_s3(url, file_type):
    print("File is getting executed.")
    file_url = ''
    
    #Get the connection of AWS S3 Bucket
    s3 = boto3.resource(
        's3',
        aws_access_key_id = keys.ACCESS_KEY_ID,
        aws_secret_access_key = keys.ACCESS_SECRET_KEY
    )
    
    response = requests.get(url)
    if response.status_code==200:
        #raw_data = response.content
        #url_parser = urlparse(url)
        #file_name = os.path.basename(url_parser.path)
        url_name = url.split('/')[-1].split('.')[0]
        flipping_image(url)
        file_name = url_name+'_transformed.jpg'
        key = file_name
        try:
            # Write the raw data as byte in new file_name in the server
            #with open(file_name, 'wb') as new_file:
                #new_file.write(raw_data)                    
            
            # Open the server file as read mode and upload in AWS S3 Bucket.
            data = open(file_name, 'rb')
            s3.Bucket(keys.AWS_BUCKET_NAME).put_object(Key=key, Body=data, ACL='public-read')
            data.close()
            
            # Format the return URL of upload file in S3 Bucket
            file_url = 'https://%s.%s/%s' % (keys.AWS_BUCKET_NAME, keys.AWS_S3_ENDPOINT, key)
            
        except Exception as e:
            print("Error in file upload %s." % (str(e)))
        
        finally:
            # Close and remove file from Server
            #os.remove(file_name)
            print("Attachment Successfully save in S3 Bucket url %s " % (file_url))
    else:
        print("Cannot parse url")
    return file_url

#url = "https://mydemoapi.s3.us-east-2.amazonaws.com/image/R_9LCVJXAiq7YyUKd.jpg"
#url = "https://mydemoapi.s3.us-east-2.amazonaws.com/image/Sample.jpg"
#file_type='image'
#upload_file_to_aws_s3(url, file_type)
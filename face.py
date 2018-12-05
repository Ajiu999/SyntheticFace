#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import base64
from json import JSONDecoder
import simplejson
import requests
import time

key = "your key"
secret = "your secret"

url = 'https://api-cn.faceplusplus.com/facepp/v3/detect'
url_add = "https://api-cn.faceplusplus.com/imagepp/v1/mergeface"

def find_face(imgpath):
	print("Processing Image")
	data = {"api_key": key, "api_secret": secret, "image_url": imgpath, "return_landmark": 1}
	files = {"image_file": open(imgpath, "rb")}
	response = requests.post(url, data=data, files=files)
	req_con = response.content.decode('utf-8')
	req_dict = JSONDecoder().decode(req_con)
	json = simplejson.dumps(req_dict)
	json2 = simplejson.loads(json)
	rectangle = json2['faces'][0]['face_rectangle']
	#print(rectangle)
	return rectangle

def synthetic_face(image_url_1,image_url_2,image_url,number):
	ff1 = find_face(image_url_1)
	time.sleep(1)   #delay
	ff2 = find_face(image_url_2)
	rectangle1 = str(str(ff1['top']) + "," + str(ff1['left']) + "," + str(ff1['width']) + "," + str(ff1['height']))
	rectangle2 = str(ff2['top']) + "," + str(ff2['left']) + "," + str(ff2['width']) + "," + str(ff2['height'])
	#print(rectangle1)
	#print(rectangle2)
	with open(image_url_1, 'rb') as file:
		f1_64 = base64.b64encode(file.read())
	with open(image_url_2, 'rb') as file:
		f2_64 = base64.b64encode(file.read())
	data = {"api_key": key, "api_secret": secret, "template_base64": f1_64, "template_rectangle": rectangle1,
			"merge_base64": f2_64, "merge_rectangle": rectangle2, "merge_rate": number}
	response = requests.post(url_add, data=data)
	req_con = response.content.decode('utf-8')
	req_dict = JSONDecoder().decode(req_con)
	#print(req_dict)
	result = req_dict['result']
	imgdata = base64.b64decode(result)
	with open(image_url, 'wb') as file:
		file.write(imgdata)

def main():
	image_url_1 = "yourIMG1.jpg"
	image_url_2 = "yourIMG2.jpg"
	image_url = 'result.jpg'
	synthetic_face(image_url_1,image_url_2,image_url,50)
	print("done!")

if __name__ == '__main__':
	main()

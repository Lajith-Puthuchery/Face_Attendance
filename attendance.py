import cv2 
import numpy as np 
import face_recognition
import os 
import pickle 
from datetime import datetime 

path = 'database'

def findencodings(images):
	encodelist = []
	for img in images:
		img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
		encoded_face = face_recognition.face_encodings(img)[0]
		encodelist.append(encoded_face)
	return encodelist

def markattendance(name):
	with open('attendance.csv', 'r+') as f:
		myDataList = f.readlines()
		namelist = []
		for line in myDataList:
			entry = line.split(',')
			namelist.append(entry[0])
		if name not in namelist:
			now = datetime.now()
			time = now.strftime('%I:%M:%S:%p')
			date = now.strftime('%d-%B-%Y')
			f.writelines('\n'+name+','+time+' '+date)


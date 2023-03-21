import cv2
import streamlit as st 
import av
from attendance import findencodings, markattendance
import face_recognition
import os
import numpy as np 
from attendance_mongo import markAttendance


cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

path = 'database'

images = []
classnames = []
mylist = os.listdir(path)
for cl in mylist:
	curimg = cv2.imread(path+'/'+cl)
	images.append(curimg)
	classnames.append(os.path.splitext(cl)[0])
print(classnames)

encoded_face_train = findencodings(images)

st.title("Webcam Application")
run = st.checkbox('Run')
FRAME_WINDOW = st.image([])
cam = cv2.VideoCapture(0)

while run:
	ret, frame = cam.read()
	frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
	imgS = cv2.resize(frame, (0,0), None, 0.25, 0.25)
	imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

	facesCurrFrame = face_recognition.face_locations(imgS)
	encodeCurrFrame = face_recognition.face_encodings(imgS,facesCurrFrame)

	for encodedFace, faceLoc in zip(encodeCurrFrame,facesCurrFrame):
		matches = face_recognition.compare_faces(encoded_face_train, encodedFace)
		faceDis = face_recognition.face_distance(encoded_face_train, encodedFace)
		matchIndex = np.argmin(faceDis)
		print

		if faceDis[matchIndex]<0.5:
			name = classnames[matchIndex].upper()
			print(name)
			y1, x1, y2, x2 = faceLoc
			y1, x1, y2, x2 = y1*4, x1*4, y2*4, x2*4 
			cv2.rectangle(frame, (x1,y1), (x2,y2), (255,255,0),3)
			cv2.rectangle(frame, (x1,y2-35), (x2,y2), (255,255,0),3)	
			cv2.putText(frame, name, (x1+6,y2-6), cv2.FONT_HERSHEY_COMPLEX, 1, (255,0,0),3)
			markAttendance(name)
	FRAME_WINDOW.image(frame)
else:
	st.write('Stopped')
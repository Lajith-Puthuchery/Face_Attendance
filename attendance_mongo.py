import pymongo
from pymongo import MongoClient
import urllib.parse
from datetime import datetime

def markAttendance(name):


	myclient = MongoClient("mongodb+srv://Lajith-FaceAttendance:"+urllib.parse.quote("B908@908")+"@cluster0.ncbqaok.mongodb.net/?retryWrites=true&w=majority")
	db = myclient["FaceAttendance"]
	now = datetime.now()
	time = now.strftime('%I:%M:%S:%p')
	date = now.strftime('%d-%B-%Y')
	collection = db[date] #Name to be Date

	post = {"Name": name, "Date":date, "Time": time}  #post with Name, Date/Time and Picture

	#Check if name already exists (if not then add to the collection)
	if collection.count_documents({"Name" : name}) == 0:
		collection.insert_one(post)

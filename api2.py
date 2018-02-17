import tweepy
import pymongo
from pprint import pprint
from pymongo import MongoClient
from queryGenerate import *
from flask import Flask
from flask import jsonify,render_template
from flask import request,Response
import pandas as pd
import datetime
import json
import bson
from bson import json_util,CodecOptions,SON
from bson.json_util import dumps
app = Flask(__name__)



@app.route('/apiForSearchUser', methods=['GET'])
def parseURL():

	#------------------------------------#

	#getting arguments from url to parse
	text=(request.args.get('text',None))
	user_name=(request.args.get('screen_name',None))
	apiUrl=request.url
	URL=apiUrl.split('?')

	#------------------------------------#

	#connecting to twitter api server

	auth = tweepy.OAuthHandler("ENTER API KEY","ENTER API SECRET KEY")
	auth.set_access_token("ENTETR ACCESS TOKEN","ENETER ACCESS SECRET TOKEN")
	api = tweepy.API(auth)



	#------------------------------------#
	#connecting to mongo server

	client = MongoClient('mongodb://localhost',27017)
	db = client.apiData
	usrDataObj = db['userData']

	#------------------------------------#


	if(text):
		for tweet in tweepy.Cursor(api.search,q=text).items():
			dataFill(tweet,usrDataObj)
	else:
		for tweet in tweepy.Cursor(api.user_timeline,screen_name=user_name).items():
			dataFill(tweet,usrDataObj)


	#------------------------------------#
	#method to handle date conversion to json

	def myconverter(o):
		if isinstance(o, datetime.datetime):
			return o.__str__()


	#------------------------------------#
	"""
	generateQuery ,module  parses the params in url and makes dictionary object
	which is same as giving combinational query using and to find method in mongodb
	"""
	dic=generateQuery(URL[1])
	cursor=db.userData.find((dic))


	#------------------------------------#

	#exporting data from database mongodb to pandas (a python library)

	df=pd.DataFrame(list(cursor))
 	df.to_csv("output_file_api2.csv",mode='w',encoding='utf-8',sep=',')


	#------------------------------------#

 	#filtered data is made as list 

 	document=[]

 	for doc in db.userData.find(dic):
 		document.append(doc)


	#------------------------------------#

 	#converting data in to json object using json.dumps method
 	#method myconverter is written to handle conversion of date to json object
 	#without myconverter method date will be like a string which is in encoded form

 	#documents=json.dumps(document, indent=4, default=json_util.default)
 	documents=json.dumps(document, indent=4, default=myconverter)



	#------------------------------------#
 	#just returning the json object

 	return documents #render_template('template.html',output=documents)


	#------------------------------------#


if __name__ == '__main__':
    app.run(debug=True)



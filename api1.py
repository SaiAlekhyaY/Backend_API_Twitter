import tweepy
import pymongo
import pprint
from pymongo import MongoClient
import re
from flask import Flask
from flask import jsonify
from flask import request
import pandas as pd
from queryGenerate import *


app = Flask(__name__)



@app.route('/apiForSearchTweet', methods=['GET'])
def parseURL():


	#-----------------------------------#
	#getting arguments from url 
	tex=(request.args.get('text',None))
	tex=str(tex)

	#------------------------------------#

	#getting access to twitter API through access tokens #here enter your own access keys
	auth = tweepy.OAuthHandler("ENTER API KEY","ENTER API SECRET KEY")
	auth.set_access_token("ENTETR ACCESS TOKEN","ENETER ACCESS SECRET TOKEN")
	api = tweepy.API(auth)


	#------------------------------------#


	def myconverter(o):
		if isinstance(o, datetime.datetime):
			return o.__str__()

	#------------------------------------#


	#setting up mongoDB server which will be listening to database connections
	client = MongoClient('mongodb://localhost',27017)
	db = client.apiData
	usrDataObj = db['userData']

	#------------------------------------#


	#getting data from API through search method according to tweettext given as param
	for tweet in tweepy.Cursor(api.search,q=tex).items():
		dataFill(tweet,usrDataObj)

	#------------------------------------#

 	#exporting data from database mongodb to pandas (a python library)

	pattern=".*"+tex+".*"
 	FilteredData=db.userData.find({"text": { "$regex" :pattern} } )
 	df=pd.DataFrame(list(FilteredData))
 	df.to_csv("output_file_api2.csv",mode='w',encoding='utf-8',sep=',')


	#------------------------------------#
 	

 	#filtered data is made as list 
 	document=[]
 	for doc in db.userData.find({"text": { "$regex" :pattern} }):
 		document.append(doc)


	#------------------------------------#


 	#converting data in to json object using json.dumps method
 	#method myconverter is written to handle conversion of date to json object
 	#without myconverter method date will be like a string which is in encoded form
 	documents=json.dumps(document, indent=4, default=myconverter)
 	

	#------------------------------------#


 	#just returning the json object
 	#can be using render_template which makes to display in webpage(template)
 	return documents #render_template('template.html',output=documents)

	#------------------------------------#



if __name__ == '__main__':
    app.run(debug=True)
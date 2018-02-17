import datetime
import time
query={}
query["$and"]=[]
flagDict={"nameStartFlag":0,"nameEndFlag":0,"textStartFlag":0,"textEndFlag":0,"screen_nameStartFlag":0,"screen_nameEndFlag":0}

#========================================================================================================================================================


def queryFill(key,value):
	di={}
	
	d = {k : v for d in query["$and"] for k, v in d.items()}

	if key in d:
		for d in query["$and"]:
			for k, v in d.items():
				if key == k:
					d[key]=value
					print(value)
	else:
		di[key]=value
		query["$and"].append(di)


#===========================================================================================================================================================

#query dictionary is filled here
def condQueryFill(key,value,op):
	di={}
	di2={}
	di[op]=value
	di2[key]=di
	query["$and"].append(di2)

#=============================================================================================================================================================


	

#===============================================================================================================================================================
#parsing regex related work

def StartsWith(key,value):
	dupKey=key+"EndFlag"
	regexDict={}
	if(flagDict[dupKey]==1):
		d = {k : v for d in query["$and"] for k, v in d.items()}
		temp=d[key]
		regex="^"+value+".*"+temp
		regexDict["$regex"]=regex
		queryFill(key,regexDict)
	else:
		regex="^"+value
		dupKey=key+"StartFlag"
		flagDict[dupKey]=1
		regexDict["$regex"]=regex

		queryFill(key,regexDict)


#================================================================================================================================================================

#parsing regex related work

def EndsWith(key,value):
	dupKey=key+"StartFlag"
	regexDict={}
	if(flagDict[dupKey]==1):
		d = {k : v for d in query["$and"] for k, v in d.items()}
		temp=d[key]
		regex=temp["$regex"]+".*"+value+"$"
		regexDict["$regex"]=regex
		queryFill(key,regexDict)
	else:
		regex=value+"$"
		dupKey=key+"EndFlag"
		flagDict[dupKey]=1
		regexDict["$regex"]=regex

		queryFill(key,regexDict)


#=======================================================================================================================================================

#parsing regex related work

def Contains(key,value):
	regexDict={}
	regex=".*"+value+".*"
	regexDict["$regex"]=regex
	queryFill(key,regexDict)


#==========================================================================================================================================================

#parsing regex related work


def Exact(key,value):
	queryFill(key,value)



#================================================================================================================================================================================

#query filling of date and relational operator is done here

def condCompare(key,value,op):
	if(len(key.split('EndDate'))>=2 or len(key.split('StartDate'))>=2 ):
		value=datetime.datetime.strptime(value, "%a %b %d %H:%M:%S +0000 %Y").date()
		print((value))
		value=(value.strftime("%Y-%m-%dT%H:%M:%S.000Z"))
		value=datetime.datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.000Z")

		condQueryFill("created_at",(value),op)


	else:
		condQueryFill(key,int(value),op)


#=========================================================================================================================================================================================

#parsing parameters based on startswith,endswith,contains,exact

def splitFunction(key,value):

	if(len(key.split('StartsWith'))>=2):
		StartsWith(key.split('StartsWith')[0],value)

	elif(len(key.split('EndsWith'))>=2):
		EndsWith(key.split('EndsWith')[0],value)
	
	elif(len(key.split('Contains'))>=2):
		Contains(key.split('Contains')[0],value)
	
	elif(len(key.split('Exact'))>=2):
		Exact(key.split('Exact')[0],value)
	else:
		if (key=="retweet_count" or key=="favourites_count"):
			queryFill(key,int(value))
		else:
			queryFill(key,(value))



#=================================================================================================================================================================================================

def generateQuery(url):
	filters=url.split('&')
	print(filters)

	#parsing url content with relational operators
	for i in filters:
		if (len(str(i).split('='))>=2):
			filterObj=str(i).split('=')
			#print(filterObj)
			splitFunction(str(filterObj[0]),filterObj[1])
		
		elif (len(str(i).split('>'))>=2):
			filterObj=i.split('>')
			condCompare(str(filterObj[0]),filterObj[1],"$gt")

		elif (len(i.split('<'))>=2):
			filterObj=i.split('<')
			condCompare(str(filterObj[0]),filterObj[1],"$lt")
	
	#clearing global content
	global query
	global flagDict

	query1={}
	query1=query

	query={}
	query["$and"]=[]
	flagDict={"nameStartFlag":0,"nameEndFlag":0,"textStartFlag":0,"textEndFlag":0,"screen_nameStartFlag":0,"screen_nameEndFlag":0}

	return query1


#=================================================================================================================================================================================================

#data populating to db
def dataFill(tweet,usrDataObj):
	data={}

	data['created_at'] = tweet.created_at
	data['favourites_count'] = (tweet.user.favourites_count)
	data['name'] = tweet.user.name
	data['text'] =tweet.text
	data['screen_name'] = tweet.user.screen_name
	data['retweet_count'] = (tweet.retweet_count)
	data['lang']=tweet.user.lang
	usrDataObj.insert(data)


#generateQuery("retweet_count=45&created_atStartDate>2016-03-06&created_atEndWith<2017-32-63&nameStartsWith=sd&nameEndsWith=r&textEndsWith=op")
#generateQuery()



		
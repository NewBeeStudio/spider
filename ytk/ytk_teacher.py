#-*- coding: utf-8 -*-
import urllib
import urllib2
import httplib
import requests
import gzip, StringIO
import cookielib
import json

root = "http://www.yuantiku.com/"
login_url = "android/users/login?platform=android21&version=1.4.0&vendor=xiao_mi&av=11&_productId=116&sign=522da99708dd4fdd3b9098d45400d4b7"
# chinese_url = "fenbi-semaphore/android/sync?platform=android19&version=5.3.0&vendor=fenbi&av=11&_productId=111&_deviceId=-1210695863610782790"
mystery_url = "ape-profile/android/phases/2/subjects/4?sprint=0&platform=android19&version=5.3.0&vendor=fenbi&av=11&_productId=111&_deviceId=-1210695863610782790"
paper_url = "fenbi-semaphore/android/sync?platform=android19&version=5.3.0&vendor=fenbi&av=11&_productId=111&_deviceId=-1210695863610782790"
stat_url = "stat"
# paper_url is samed as chinese_url

def gzipdecode(data):
	compressedstream = StringIO.StringIO(data)
	gziper = gzip.GzipFile(fileobj = compressedstream)  
	ans = gziper.read()   
	return ans 

def getRequest(url, name, getSid = False):
	final = root + url
	# final = "http://yuantiku.com/tarzan/android/solutions/bundle?ids=1758221%2C1758245%2C1758247%2C1758251%2C1758257%2C1758263%2C1758271%2C1758275%2C1758281%2C1758283%2C512173%2C512261%2C512269%2C512287%2C512293%2C597345%2C860325%2C832289%2C660591%2C862509%2C1332397%2C1749841%2C784247%2C466047%2C1144957%2C837469%2C1744979%2C1744981%2C1744985%2C1744987%2C1744991%2C1744993%2C1744997%2C1745001%2C1745003%2C1745007%2C858989&platform=android21&version=1.4.0&vendor=xiao_mi&av=11&_productId=116&sign=7ac77753add901c8b7f14137869e8cff"
	request_index = urllib2.Request(root + url)

	request_index.add_header('User-Agent', 'gandalf-android')
	request_index.add_header('Accept-Encoding', 'gzip')
	request_index.add_header('Host', 'yuantiku.com')
	request_index.add_header('Connection', 'Keep-Alive')
	request_index.get_method = lambda: 'GET'
	response_index = urllib2.urlopen(request_index)
	if getSid:
		print response_index.info()
	text = gzipdecode(response_index.read())
	index_data = json.loads(text)
	print name, "!"
	with open(name+'.html', 'w') as outfile:
	    json.dump(index_data, outfile)
	response_index.close()

cookie = cookielib.CookieJar()
handler = urllib2.HTTPCookieProcessor(cookie)
opener = urllib2.build_opener(handler)
urllib2.install_opener(opener)

# 登录

values = {'phone': '15026613197', 
		'password': 'ZuNebqY6m51lRFoXeqrHZ7RfY+H7LHZbCtSrHQOCJJeXL2qc1l6tTjsqgYQnPjI+ydmeBdeDhOqSpFDaI3/KSTqAhp5patlhATRfkAjT5gPTotnXoZr1xK/g2Qu6apQfdR1eaH3+qUixt3nokJXhp8bnE7UeN8ODeoQtYih0mR0=',
		'persistent': 'true',
		'device': 'android%3Ateacher%3Awzx2Sn1UH3m0l3fJKFM6YA%3D%3D'
		}
request_login = urllib2.Request(root + login_url, urllib.urlencode(values))

request_login.add_header('User-Agent', 'gandalf-android')
request_login.add_header('Accept-Encoding', 'gzip')
request_login.add_header('Host', 'yuantiku.com')
request_login.add_header('Connection', 'Keep-Alive')

response_login = urllib2.urlopen(request_login)

text = gzipdecode(response_login.read())
login_data = json.loads(text)
co = response_login.info()['Set-Cookie']
sess = co.split('sess=')[1].split(';')[0]
userid = co.split('userid=')[1].split(';')[0]
persistent = co.split('persistent=')[1].split(';')[0]
print "login data: ", login_data

index_url = 'tarzan/android/keypoints/stat?phaseId=1&subjectId=3&courseBookId=1303&platform=android21&version=1.4.0&vendor=xiao_mi&av=11&_productId=116'

getRequest(index_url, 'teacher_index')

types = "gandalf-sphinx/android/questions/types?groupId=11445350&courseBookId=1303&keypointIds=609911&platform=android21&version=1.4.0&vendor=xiao_mi&av=11&_productId=116"
getRequest(types, "teacher_types", getSid=True)

pick_url = "gandalf-sphinx/android/questions/pick?groupId=11445350&courseBookId=1303&keypointIds=609911&page=0&pageSize=15&platform=android21&version=1.4.0&vendor=xiao_mi&av=11&_productId=116"
getRequest(pick_url, "teacher_pick")

sol_url = 'tarzan/android/solutions/bundle?ids=882827%2C502389%2C502393%2C502403%2C502407%2C502409%2C502413%2C502417%2C502427%2C502433%2C502439%2C499309%2C499323%2C499329%2C499337%2C499353%2C499357%2C499363%2C499371%2C499381%2C499391%2C886057%2C886065%2C886071%2C886077%2C886085%2C886101%2C886109%2C886113%2C886123%2C886129%2C836867%2C1329579%2C784233%2C552891%2C552899%2C552905%2C552909%2C552913%2C552921%2C552923%2C552931%2C552935%2C552945%2C1352447%2C1335725%2C879227%2C656155%2C656167%2C656185%2C1333355%2C1273643%2C1273645%2C1273647%2C1273649%2C1273653%2C772259&platform=android21&version=1.4.0&vendor=xiao_mi&av=11&_productId=116&sign=277b4bf0645d7e25067b0cf3732a74f9'
sol_url = "tarzan/android/solutions/bundle?ids=616447%2C611289%2C612325%2C612337%2C612351%2C612361%2C612375%2C612381%2C612391%2C612407%2C612415%2C612425%2C612439%2C612445%2C504301%2C831227%2C878259%2C655327%2C541627%2C855627%2C770313%2C1728265%2C459597%2C855617%2C831205%2C586917%2C586925%2C586931%2C586945%2C586957&platform=android21&version=1.4.0&vendor=xiao_mi&av=11&_productId=116&sign=6ea272d39158ecae8b56ba5a647afa87"

getRequest(sol_url, "teacher_sol")

ana_url = "ape-group-question-stat/android/groups/11445350/questions/stat?questionIds=882827%2C502389%2C502393%2C502403%2C502407%2C502409%2C502413%2C502417%2C502427%2C502433%2C502439%2C499309%2C499323%2C499329%2C499337%2C499353%2C499357%2C499363%2C499371%2C499381%2C499391%2C886057%2C886065%2C886071%2C886077%2C886085%2C886101%2C886109%2C886113%2C886123%2C886129%2C836867%2C1329579%2C784233%2C552891%2C552899%2C552905%2C552909%2C552913%2C552921%2C552923%2C552931%2C552935%2C552945%2C1352447%2C1335725%2C879227%2C656155%2C656167%2C656185%2C1333355%2C1273643%2C1273645%2C1273647%2C1273649%2C1273653%2C772259&platform=android21&version=1.4.0&vendor=xiao_mi&av=11&_productId=116"
getRequest(ana_url, "teacher_ana")
# print "index data: ", index_data








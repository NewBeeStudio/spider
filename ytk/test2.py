#-*- coding: utf-8 -*-
import urllib
import urllib2
import gzip, StringIO
import cookielib
import json

root = "http://www.yuantiku.com/"

login_url = "android/users/login?platform=android19&version=5.3.0&vendor=fenbi&av=11&_productId=111&_deviceId=-1210695863610782790&sign=8435cf769b7888e8d74a8282f414ebe1"
# chinese_url = "fenbi-semaphore/android/sync?platform=android19&version=5.3.0&vendor=fenbi&av=11&_productId=111&_deviceId=-1210695863610782790"
mystery_url = "ape-profile/android/phases/2/subjects/4?sprint=0&platform=android19&version=5.3.0&vendor=fenbi&av=11&_productId=111&_deviceId=-1210695863610782790"
physical_url = "android/gzwl/users/keypoint-tree?deep=true&platform=android19&version=5.3.0&vendor=fenbi&av=11&_productId=111&_deviceId=-1210695863610782790"
paper_url = "fenbi-semaphore/android/sync?platform=android19&version=5.3.0&vendor=fenbi&av=11&_productId=111&_deviceId=-1210695863610782790"
stat_url = "stat"
# paper_url is samed as chinese_url

def gzipdecode(data):
	compressedstream = StringIO.StringIO(data)
	gziper = gzip.GzipFile(fileobj = compressedstream)  
	ans = gziper.read()   
	return ans 

values = {'phone': '13122262056', 
		'password': 'OJg3TlbbGzavD+pvUAm4Mc6/+dnbgiOd9TQW8O7B48R13skyAeGgPCQ1LHbEZ1MxcInsPRl2qvGD4itujTtzOfVVsX4w+y3Te8ig90i1V0smk+Omc7UwSWT1wPPNT0M1ukfMMif/FAMZaVIWICbrMs2Wik/MQmebL5eofLTWfi0=',
		'persistent': 'true'}
values2 = {'phone': '15026613197', 
		'password': 'TaBXhwAhfvj9xfi7mHxwyHXZXlDrGNfWh3VhVY3AVnEChcVDwieLhdao0KeBmZn7RKNYOgddpCC6BJWEmOS+prVF/+XFuTQOG0Uu/j4+1nth0ngiF9ey//gBbeEdpON3qxmfkk68Vhdz4CVUblZ99a6t8JqIfyIEpYlOKeZ4AeU=',
		'persistent': 'true'}
data = urllib.urlencode(values2)

cookie = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
urllib2.install_opener(opener)

# 登录

request_login = urllib2.Request(root + login_url, data)

request_login.add_header('User-Agent', 'ape-android')
# request_login.add_header('Accept-Encoding', 'none') 这样可能被发现_(:з」∠)_
request_login.add_header('Accept-Encoding', 'gzip')
request_login.add_header('Host', 'www.yuantiku.com')
request_login.add_header('Connection', 'Keep-Alive')

response_login = urllib2.urlopen(request_login)

text = gzipdecode(response_login.read())
login_data = json.loads(text)



'''
# 获取状态 这个要send一大堆数据，还没搞清楚是什么_(:з」∠)_

request_stat = urllib2.Request(root + stat_url)

request_stat.add_header('User-Agent', 'ape-android')
request_stat.add_header('Accept-Encoding', 'gzip')
# request_stat.add_header('Content-Encoding', 'gzip')
request_stat.add_header('Host', 'frog.yuantiku.com')
request_stat.add_header('Connection', 'Keep-Alive')
request_stat.add_header('Content-Type', 'application/json;charset=UTF-8')

# request_stat.get_method = lambda: 'POST'
response_stat = urllib2.urlopen(request_stat)
text = gzipdecode(response_stat.read())
print text
stat_data = json.loads(text)
print stat_data
'''
'''
# 单击语文 有cache 没办法第二次模拟，先试一下物理

request_chinese = urllib2.Request(root + chinese_url)

request_chinese.add_header('User-Agent', 'ape-android')
request_chinese.add_header('Accept-Encoding', 'gzip')
request_chinese.add_header('Host', 'www.yuantiku.com')
request_chinese.add_header('Connection', 'Keep-Alive')
request_chinese.add_header('Content-Type', 'application/json;charset=UTF-8')
request_chinese.add_header('Server', 'YTK')

# request_chinese.get_method = lambda: 'GET'

response_chinese = urllib2.urlopen(request_chinese)
text = gzipdecode(response_chinese.read())
print text
chinese_data = json.loads(text)
print chinese_data
'''

# chinese_url = "android/czyw/questions/bundle?exerciseId=505603002&treeId=267&ids=538145%2C711321%2C574417%2C705801%2C854629&platform=android21&version=5.3.0&vendor=xiao_mi&av=11&_productId=111&_deviceId=7254182039677307575&sign=097c47797"

# request_chinese = urllib2.Request(root + chinese_url)

# request_chinese.add_header('User-Agent', 'ape-android')
# request_chinese.add_header('Accept-Encoding', 'gzip')
# request_chinese.add_header('Host', 'www.yuantiku.com')
# request_chinese.add_header('Connection', 'Keep-Alive')

# request_chinese.get_method = lambda: 'GET'

# responce_chinese = urllib2.urlopen(request_chinese)
# text = gzipdecode(responce_chinese.read())
# # print text
# chinese_data = json.loads(text)
# print chinese_data


# 单击物理 成功_(:з」∠)_

request_mystery = urllib2.Request(root + mystery_url)

request_mystery.add_header('User-Agent', 'ape-android')
request_mystery.add_header('Accept-Encoding', 'gzip')
request_mystery.add_header('Host', 'www.yuantiku.com')
request_mystery.add_header('Connection', 'Keep-Alive')

request_mystery.get_method = lambda: 'PUT'

response_mystery = urllib2.urlopen(request_mystery)

request_physical = urllib2.Request(root + physical_url)

request_physical.add_header('User-Agent', 'ape-android')
request_physical.add_header('Accept-Encoding', 'gzip')
request_physical.add_header('Host', 'www.yuantiku.com')
request_physical.add_header('Connection', 'Keep-Alive')

request_physical.get_method = lambda: 'GET'

response_physical = urllib2.urlopen(request_physical)
text = gzipdecode(response_physical.read())
# print text
physical_data = json.loads(text)
# print physical_data

# 单击“语文” -> “字音辨析” 失败了 我明明Connection写的是Keep-Alive, 但是在抓包里边就变成了close 不知道为什么 
zybx_url_1 = "android/gzyw/exercises?platform=android19&version=5.3.0&vendor=fenbi&av=11&_productId=111&_deviceId=-1210695863610782790"
zybx_values = {"type": "3",
	"keypointId": "91937420",
	"treeId": "215",
	"limit": "5"}
request_zybx_1 = urllib2.Request(root + zybx_url_1, urllib.urlencode(zybx_values))

request_zybx_1.add_header('Accept-Encoding', 'gzip')
request_zybx_1.add_header('Content-Type', 'application/x-www-form-urlencoded')
request_zybx_1.add_header('Host', 'www.yuantiku.com')
request_zybx_1.add_header('Connection', 'Keep-Alive')
request_zybx_1.add_header('User-Agent', 'ape-android')

response_zybx_1 = urllib2.urlopen(request_zybx_1)
text = gzipdecode(response_zybx_1.read())
# print text
zybx_1_data = json.loads(text)
print zybx_1_data

# 单击试卷 OK

values = {"deviceId": "-1210695863610782790",
		"cursorTime": 1447431144000,
		"userId": 46207413}

request_paper = urllib2.Request(root + paper_url, json.dumps(values))

request_paper.add_header('User-Agent', 'ape-android')
request_paper.add_header('Accept-Encoding', 'gzip')
request_paper.add_header('Host', 'www.yuantiku.com')
request_paper.add_header('Connection', 'Keep-Alive')
request_paper.add_header('Content-Type', 'application/json;charset=UTF-8')

# request_chinese.get_method = lambda: 'GET'

response_paper = urllib2.urlopen(request_paper)
text = gzipdecode(response_paper.read())
paper_data = json.loads(text)
print paper_data



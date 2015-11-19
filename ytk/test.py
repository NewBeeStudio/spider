#-*- coding: utf-8 -*-
import urllib
import urllib2
import requests
import gzip, StringIO
# import httpio
import cookielib
import json

root = "http://www.yuantiku.com/"
# conn = HTTPConnection(root)
login_url = "android/users/login?platform=android19&version=5.3.0&vendor=fenbi&av=11&_productId=111&_deviceId=-1210695863610782790&sign=8435cf769b7888e8d74a8282f414ebe1"
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

values = {'phone': '13122262056', 
		'password': 'OJg3TlbbGzavD+pvUAm4Mc6/+dnbgiOd9TQW8O7B48R13skyAeGgPCQ1LHbEZ1MxcInsPRl2qvGD4itujTtzOfVVsX4w+y3Te8ig90i1V0smk+Omc7UwSWT1wPPNT0M1ukfMMif/FAMZaVIWICbrMs2Wik/MQmebL5eofLTWfi0=',
		'persistent': 'true'}
values2 = {'phone': '15026613197', 
		'password': 'TaBXhwAhfvj9xfi7mHxwyHXZXlDrGNfWh3VhVY3AVnEChcVDwieLhdao0KeBmZn7RKNYOgddpCC6BJWEmOS+prVF/+XFuTQOG0Uu/j4+1nth0ngiF9ey//gBbeEdpON3qxmfkk68Vhdz4CVUblZ99a6t8JqIfyIEpYlOKeZ4AeU=',
		'persistent': 'true'}
data = urllib.urlencode(values2)

cookie = cookielib.CookieJar()
handler = urllib2.HTTPCookieProcessor(cookie)
opener = urllib2.build_opener(handler)
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
response_login.close()
login_data = json.loads(text)
co = response_login.info()['Set-Cookie']
sess = co.split('sess=')[1].split(';')[0]
userid = co.split('userid=')[1].split(';')[0]
persistent = co.split('persistent=')[1].split(';')[0]
Domain = '".yuantiku.com"'
Path = '"/"'

# 单击物理 成功_(`:з」∠)_

# physical_outline_url = "android/gzwl/users/keypoint-tree?deep=true&platform=android19&version=5.3.0&vendor=fenbi&av=11&_productId=111&_deviceId=-1210695863610782790"
# physical_url = "android/czwl/questions/bundle?exerciseId=505641776&treeId=273&ids=1387445%2C1386881%2C1387317%2C1387329%2C1500749&platform=android21&version=5.3.0&vendor=xiao_mi&av=11&_productId=111&_deviceId=7254182039677307575&sign=bf0a"

# # 单击“语文” -> “字音辨析” 失败了 我明明Connection写的是Keep-Alive, 但是在抓包里边就变成了close 不知道为什么 
# zybx_url_1 = "android/gzyw/exercises?platform=android19&version=5.3.0&vendor=fenbi&av=11&_productId=111&_deviceId=-1210695863610782790"
zybx_url_1 = "android/zksx/exercises?platform=android21&version=5.3.0&vendor=xiao_mi&av=11&_productId=111&_deviceId=7254182039677307575"
zybx_values = {"type": "3",
	"keypointId": "159289",
	"treeId": "953",
	"limit": "5"}
request_zybx_1 = urllib2.Request(root + zybx_url_1, urllib.urlencode(zybx_values))

request_zybx_1.add_header('Accept-Encoding', 'gzip')
request_zybx_1.add_header('Content-Type', 'application/x-www-form-urlencoded')
request_zybx_1.add_header('Host', 'www.yuantiku.com')
request_zybx_1.add_header('Connection', 'Keep-Alive')
# request_zybx_1.add_header('Cookie', co)
request_zybx_1.add_header('User-Agent', 'ape-android')

response_zybx_1 = urllib2.urlopen(request_zybx_1)
response_zybx_1.close()
cook = response_zybx_1.info()['Set-Cookie']
sid = cook.split("sid=")[1].split(";")[0]

zybx_url_2 = "android/czsx/questions/bundle?exerciseId=507083004&treeId=315&ids=1374593%2C1374373%2C1374247%2C1374157%2C1374217&platform=android21&version=5.3.0&vendor=xiao_mi&av=11&_productId=111&_deviceId=7254182039677307575&sign=623f63b66bc183243eccf514dddb33c0"
# zybx_values = {"ids": [916213,944987,942581,950273,978539]}
request_zybx_2 = urllib2.Request(root + zybx_url_2)

request_zybx_2.add_header('Accept-Encoding', 'gzip')
# request_zybx_2.add_header('Content-Encoding', 'gzip')
# request_zybx_2.add_header('Content-Length', len(jsonbytes))
# request_zybx_2.add_header('Transfer-Encoding', 'chunked')
# request_zybx_2.add_header('Content-Type', 'application/json; charset=utf-8')
request_zybx_2.add_header('Host', 'www.yuantiku.com')
request_zybx_2.add_header('Connection', 'Keep-Alive')
request_zybx_2.add_header('User-Agent', 'ape-android')
request_zybx_2.add_header('Expect', "false")
# cookie.clear()
final_co = "sid="+sid+"; userid="+userid+'; sess="'+sess+'"; $Path='+Path+"; $Domain="+Domain+"; persistent="+persistent[1:-1]
final_head = {"Accept-Encoding": "gzip", "Host": "www.yuantiku.com", "Connection": "Keep-Alive", "User-Agent": "ape-android", "Cookie": final_co}
# r = requests.get(root+zybx_url_2, headers=final_head)
# request_zybx_2.add_header('Cookie', final_co)
# # print jsonbytes
# responce_zybx_2 = urllib2.urlopen(request_zybx_2)
# text = gzipdecode(responce_zybx_2.read())
# data = json.load(text)
paper_url = "android/zksx/exercises?platform=android21&version=5.3.0&vendor=xiao_mi&av=11&_productId=111&_deviceId=7254182039677307575"
paper_url = "android/zksx/questions/bundle?exerciseId=55950623&treeId=953&ids=947917%2C947941%2C947981%2C948031%2C948063%2C948091%2C948119%2C948137%2C948181%2C948207%2C948243%2C948283%2C927037%2C948401%2C948547%2C948589%2C948621%2C948691%2C948749%2C948791%2C948841&platform=android21&version=5.3.0&vendor=xiao_mi&av=11&_productId=111&_deviceId=7254182039677307575&sign=c1eb7d4a65a03995d2684cc6f37d0e32"
r = requests.post(root+paper_url, data={"type": "1", "paperId": "69445"}, headers=final_head)
print r.text


# chinese_url = "android/czwl/questions/bundle?exerciseId=505658794&treeId=273&ids=1392855%2C1393785%2C1393885%2C1394079%2C1392651&platform=android21&version=5.3.0&vendor=xiao_mi&av=11&_productId=111&_deviceId=7254182039677307575&sign=6312"
# chinese_url = "android/zkwl/questions/info?platform=android21&version=5.3.0&vendor=xiao_mi&av=11&_productId=111&_deviceId=7254182039677307575"
# cookies = {'sess': '3eFB/bXKvpukXLGh/C1caJidtg1tzRXVQO2iLwgcIs9Bjnbt4mbU5Z2xyuUfsj+O', 'userid': 46679127, 'persistent': "Ok3fk1xi/5m1PvYnU3hBzknaUebhXFBS4G8VaFzj9BK6QrnHcIxH6Alw2TpTOF9/BuSyEDzu0Wekt3h+Ts1ZhQ==", 'sid': 4120753229618361916}
# val = {"ids": "1226463,1352407,1234411,975533,1053197"}



response_paper = urllib2.urlopen(request_paper)
text = gzipdecode(response_paper.read())
paper_data = json.loads(text)
# print paper_data
with open('chinese.json', 'w') as outfile:
    json.dump(paper_data, outfile)




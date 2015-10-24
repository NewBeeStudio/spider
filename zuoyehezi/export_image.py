import os, sys
import mysql.connector


user = 'root'
password = ''
directory = 'images'


if not os.path.exists(directory):
	os.mkdir(directory)

cnx = mysql.connector.connect(user = user, password = password, host = '127.0.0.1', database = 'ZYHZ')
cursor = cnx.cursor(buffered = True)
cursor2 = cnx.cursor()
sql = "SELECT id, data FROM image;"

cursor.execute(sql)

cnt = 0

for (ID, data) in cursor:
	cnt += 1
	print 'processing ', cnt
	filename = 'images/%s.jpg' % ID

	img = open(filename, 'wb')
	img.write(data)
	img.close()
	sql = "INSERT INTO image_url (url) VALUES ('%s') " % ID
	cursor2.execute(sql)
cnx.commit()


cursor.close()
cnx.close()

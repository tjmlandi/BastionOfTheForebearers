import mysql.connector
from mysql.connector import errorcode


try:
	cnx = mysql.connector.connect(user='root',password='password',database='players')
	cursor = cnx.cursor()
	
	user = raw_input("Please Enter Your Username: ")
	pword = raw_input("Please Enter Your Password: ")
	
	query = ('SELECT * FROM gold WHERE username="' + user + '" AND password="' + pword + '"')]
	cursor.execute(query)
	
	#while true:
	#	cmd = raw_input("~: ")
		
		
	#	query = ("SELECT * FROM gold")
		
		
except mysql.connector.Error as err:
	if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
		print "Your username or password is incorrect"
	elif err.errno == errorcode.ER_BAD_DB_ERROR:
		print "Database does not exist"
	else:
		print err
else:
	cnx.close()
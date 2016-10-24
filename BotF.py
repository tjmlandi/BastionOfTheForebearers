import mysql.connector
from mysql.connector import errorcode


try:
	cnx = mysql.connector.connect(user='root',password='password',database='players')
	cursor = cnx.cursor(buffered=True)
	while True:
		user = raw_input("Please Enter Your Username: ")
		pword = raw_input("Please Enter Your Password: ")
		
		queryGold = ('SELECT * FROM gold WHERE username="' + user + '" AND password="' + pword + '"')
		querySilver = ('SELECT * FROM silver WHERE username="' + user + '" AND password="' + pword + '"')
		queryBronze = ('SELECT * FROM bronze WHERE username="' + user + '" AND password="' + pword + '"')
		
		cursor.execute(queryGold)
		inGold = (cursor.rowcount > 0)
		if inGold:
			user = cursor.next()
		
		cursor.execute(querySilver)
		inSilver = (cursor.rowcount > 0)
		if inSilver:
			user = cursor.next()
		
		cursor.execute(queryBronze)
		inBronze = (cursor.rowcount > 0)
		if inBronze:
			user = cursor.next()
		
		if inGold or inSilver or inBronze:
			break
		else:
			print "Usernamr or Password is incorrect"
	
	while True:
		command = raw_input("~:")
		if command == "help":
			print "Available Commands:"
			print "exit: Ends Program"
		elif command == "exit":
			print "Goodbye"
			break
	
	
		
		
except mysql.connector.Error as err:
	if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
		print "Your username or password is incorrect"
	elif err.errno == errorcode.ER_BAD_DB_ERROR:
		print "Database does not exist"
	else:
		print err
else:
	cnx.close()
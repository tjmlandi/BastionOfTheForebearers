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
			league = 'gold'
		
		cursor.execute(querySilver)
		inSilver = (cursor.rowcount > 0)
		if inSilver:
			user = cursor.next()
			league = 'silver'
		
		cursor.execute(queryBronze)
		inBronze = (cursor.rowcount > 0)
		if inBronze:
			user = cursor.next()
			league = 'bronze'
		
		if inGold or inSilver or inBronze:
			break
		else:
			print "Username or Password is incorrect"
	
	add_player = ("INSERT INTO online_players "
			"(player_id, league) "
			"VALUES (%s, %s)")
	data_player = (user[0], league)
	cursor.execute(add_player, data_player)
	cnx.commit()
	
	while True:
		command = raw_input("~:")
		if command == "help":
			print "Available Commands:"
			print "exit: Ends Program"
		elif command == "exit":
			print "Goodbye"
			delete_player = ("DELETE FROM online_players WHERE player_id = " + str(user[0]))
			cursor.execute(delete_player)
			cnx.commit()
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
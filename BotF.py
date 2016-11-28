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
			print "Available Commands: view_online, view_stats, queue, queue_season"
			print "exit: Ends Program"
		elif command == "queue":
			
		elif command == "view_stats":
			print "%s, - %s League" % (user[1], league)
			print "ELO: %d - Wins: %d - Losses: %d, Preferred Role: %s" % (user[3], user[4], user[5], user[7])
		elif command == "view_online":
			print "Gold Players Online:"
			cursor.execute("select * from gold, online_players where gold.player_id = online_players.player_id and online_players.league = 'gold'")
			results = cursor.fetchall()
			for row in results:
			  fname = row[1]
			  # Now print fetched result
			  print "%s" % \
					 (fname)
			print "Silver Players Online:"
			cursor.execute("select * from silver, online_players where silver.player_id = online_players.player_id and online_players.league = 'silver'")
			results = cursor.fetchall()
			for row in results:
			  fname = row[1]
			  # Now print fetched result
			  print "%s" % \
					 (fname)
			print "Bronze Players Online:"
			cursor.execute("select * from bronze, online_players where bronze.player_id = online_players.player_id and online_players.league = 'bronze'")
			results = cursor.fetchall()
			for row in results:
			  fname = row[1]
			  # Now print fetched result
			  print "%s" % \
					 (fname)
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
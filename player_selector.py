import mysql.connector
from mysql.connector import errorcode

def player_selector(middleElo, league):
	try:
		cnx = mysql.connector.connect(user='root',password='password',database='players')
		cursor = cnx.cursor(buffered=True)
		bound = 75
		playersFound = 0
		players = [[0 for x in range(5)] for y in range(2)]
		while playersFound == 0:
			
			upper = middleElo + bound
			lower = middleElo - bound
			
			query = ('SELECT * FROM ' + league + ' WHERE elo>' + str(lower) + ' AND elo<' + str(upper) + ' ORDER BY RAND()')
			
			cursor.execute(query)
			
			playerCount = cursor.rowcount
						
			if playerCount >= 10:
				for x in range(0,5):
					players[0].insert(x, cursor.next())
				for x in range(0,5):
					players[1].insert(x, cursor.next())
				playersFound = 1
				
			bound += 10
		cnx.commit()
		
	except mysql.connector.Error as err:
		if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
			print "Your username or password is incorrect"
		elif err.errno == errorcode.ER_BAD_DB_ERROR:
			print "Database does not exist"
		else:
			print err
	else:
		cnx.close()
		
	return players
	
def online_player_selector(middleElo, league):
	try:
		cnx = mysql.connector.connect(user='root',password='password',database='players')
		cursor = cnx.cursor(buffered=True)
		bound = 75
		playersFound = 0
		players = [[0 for x in range(5)] for y in range(2)]
		while playersFound == 0:
			
			upper = middleElo + bound
			lower = middleElo - bound
			
			query = ('SELECT * FROM online_players WHERE elo>' + str(lower) + ' AND elo<' + str(upper) + ' AND league="' + league + '" ORDER BY RAND()')
			
			cursor.execute(query)
			
			playerCount = cursor.rowcount
						
			if playerCount >= 10:
				for x in range(0,5):
					players[0].insert(x, cursor.next())
				for x in range(0,5):
					players[1].insert(x, cursor.next())
				playersFound = 1
				
			bound += 10
		cnx.commit()
		
	except mysql.connector.Error as err:
		if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
			print "Your username or password is incorrect"
		elif err.errno == errorcode.ER_BAD_DB_ERROR:
			print "Database does not exist"
		else:
			print err
	else:
		cnx.close()
		
	return players
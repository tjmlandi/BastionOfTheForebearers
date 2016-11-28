import mysql.connector
from mysql.connector import errorcode

def player_selector(middleElo, league):
	try:
		cnx = mysql.connector.connect(user='root',password='password',database='players')
		cursor = cnx.cursor(buffered=True)
		
		upper = middleElo + 75
		lower = middleElo - 75
		
		query = ('SELECT * FROM ' + league + ' WHERE elo>' + str(lower) + ' AND elo<' + str(upper) + ' ORDER BY RAND()')
		
		cursor.execute(query)
		
		playerCount = cursor.rowcount
		
		players = [10]
		
		if playerCount > 10:
			for x in range(0,10):
				players.insert(x, cursor.next())
			
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
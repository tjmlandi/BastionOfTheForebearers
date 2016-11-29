import mysql.connector
from mysql.connector import errorcode
import random
import player_selector


	
def MatchMaker(playerid,league,elo):
	try:
		cnx = mysql.connector.connect(user='root',password='password',database='players')
		cursor = cnx.cursor(buffered=True)

		players=player_selector.online_player_selector(elo,playerid, league)

		teamOne = 0 
		teamTwo = 0
		teamOneElo = 0
		teamTwoElo = 0
		for one in range(0,5):
			teamOne += players[0][one][6]
			teamOneElo += players[0][one][3]
		for two in range(0,5):
			teamTwo += players[1][two][6]
			teamTwoElo += players[1][two][3]
		if max(teamOne, teamTwo) == teamOne:
			skillTeam = 0
			noSkillTeam = 1
		else:
			skillTeam = 1
			noSkillTeam = 0
		chance = 50 + abs(teamOne - teamTwo)
		result = random.randint(0,100)
		eloAdj = abs(teamOneElo - teamTwoElo) / 6
		if result < chance:
			#print 'High skill team won'
			for x in range(0,5):
				#print players[skillTeam][x][0]
				#print players[skillTeam][x][3]
				query = ('UPDATE ' + league + ' SET wins=wins + 1 ' + ' WHERE player_id=' + str(players[skillTeam][x][0]))
				cursor.execute(query)
				query = ('UPDATE ' + league + ' SET elo=elo + ' + str(eloAdj) + ' WHERE player_id=' + str(players[skillTeam][x][0]))
				cursor.execute(query)
			for x in range(0,5):
				#print players[noSkillTeam][x][0]
				#print players[noSkillTeam][x][3]
				query = ('UPDATE ' + league + ' SET losses=losses + 1 ' + ' WHERE player_id=' + str(players[noSkillTeam][x][0]))
				cursor.execute(query)
				query = ('UPDATE ' + league + ' SET elo=elo - ' + str(eloAdj) + ' WHERE player_id=' + str(players[noSkillTeam][x][0]))
				cursor.execute(query)
		else:
			for x in range(0,5):
				#print players[noSkillTeam][x][0]
				#print players[noSkillTeam][x][3]
				query = ('UPDATE ' + league + ' SET wins=wins + 1 ' + ' WHERE player_id=' + str(players[noSkillTeam][x][0]))
				cursor.execute(query)
				query = ('UPDATE ' + league + ' SET elo=elo + ' + str(eloAdj) + ' WHERE player_id=' + str(players[noSkillTeam][x][0]))
				cursor.execute(query)
			for x in range(0,5):
				#print players[skillTeam][x][0]
				#print players[skillTeam][x][3]
				query = ('UPDATE ' + league + ' SET losses=losses + 1 ' + ' WHERE player_id=' + str(players[skillTeam][x][0]))
				cursor.execute(query)
				query = ('UPDATE ' + league + ' SET elo=elo - ' + str(eloAdj) + ' WHERE player_id=' + str(players[skillTeam][x][0]))
				cursor.execute(query)
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
		



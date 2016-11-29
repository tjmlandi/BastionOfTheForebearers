import mysql.connector
import player_selector
import random
from mysql.connector import errorcode

import mysql.connector
from mysql.connector import errorcode

#Bastion of the Forerunners
try:
	cnx = mysql.connector.connect(user='root',password='password',database='players')
	cursor = cnx.cursor(buffered=True)
	while True:
		command = raw_input("~:")
		if command == "simulate":
			for iterations in range(0,100):
				print iterations
				for leagues in range(0,3):
					if leagues == 0:
						league = 'bronze'
					if leagues == 1:
						league = 'silver'
					if leagues == 2:
						league = 'gold'
					for inner in range(0,10):
						elo = (2000 * leagues) + (inner * 200)
						players = player_selector.player_selector(elo, league)
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
							#print 'Low skill team won'
						
						cnx.commit()	
			query = ('INSERT INTO silver SELECT * from bronze where elo>2000')
			cursor.execute(query)
			query = ('DELETE FROM bronze WHERE elo>2000')
			cursor.execute(query)
			cnx.commit()
			query = ('INSERT INTO bronze SELECT * from silver where elo<2000')
			cursor.execute(query)
			query = ('DELETE FROM silver WHERE elo<2000')
			cursor.execute(query)
			cnx.commit()
			
			query = ('INSERT INTO gold SELECT * from silver where elo>4000')
			cursor.execute(query)
			query = ('DELETE FROM silver WHERE elo>4000')
			cursor.execute(query)
			cnx.commit()
			query = ('INSERT INTO silver SELECT * from gold where elo<4000')
			cursor.execute(query)
			query = ('DELETE FROM gold WHERE elo<4000')
			cursor.execute(query)
			cnx.commit()
			
		elif command == "help":
			print "Available Commands:"
			print "exit: Ends Program"
		elif command == "exit":
			print "Goodbye"
			break
		else:
			print "Command not recongnized, enter 'help' in order to view valid commands"
	
	
		
		
except mysql.connector.Error as err:
	if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
		print "Your username or password is incorrect"
	elif err.errno == errorcode.ER_BAD_DB_ERROR:
		print "Database does not exist"
	else:
		print err
else:
	cnx.close()
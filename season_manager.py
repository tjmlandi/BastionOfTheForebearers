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
			for l in range(0,3):
				if l == 0:
					league = 'bronze'
				if l == 1:
					league = 'silver'
				if l == 2:
					league = 'gold'
				for i in range(0,10):
					elo = (2000 * l) + (i * 200)
					players = player_selector.player_selector(elo, league)
					teamOne = 0 
					teamTwo = 0
					for x in range(0,5):
						teamOne += players[0][x][6]
					for x in range(0,5):
						teamTwo += players[1][x][6]
					if max(teamOne, teamTwo) == teamOne:
						skillTeam = 0
						noSkillTeam = 1
					else:
						skillTeam = 1
						noSkillTeam = 0
					chance = 50 + abs(teamOne - teamTwo)
					result = random.randint(0,100)
					if result < chance:
						print 'High skill team won'
						for x in range(0,5):
							print players[skillTeam][x][0]
							query = ('UPDATE ' + league + ' SET wins=wins + 1 ' + ' WHERE player_id=' + str(players[skillTeam][x][0]))
							cursor.execute(query)
						for x in range(0,5):
							print players[noSkillTeam][x][0]
							query = ('UPDATE ' + league + ' SET losses=losses + 1 ' + ' WHERE player_id=' + str(players[noSkillTeam][x][0]))
							cursor.execute(query)
					else:
						for x in range(0,5):
							print players[noSkillTeam][x][0]
							query = ('UPDATE ' + league + ' SET wins=wins + 1 ' + ' WHERE player_id=' + str(players[noSkillTeam][x][0]))
							cursor.execute(query)
						for x in range(0,5):
							print players[skillTeam][x][0]
							query = ('UPDATE ' + league + ' SET losses=losses + 1 ' + ' WHERE player_id=' + str(players[skillTeam][x][0]))
							cursor.execute(query)
						print 'Low skill team won'
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
import mysql.connector
import player_selector
from mysql.connector import errorcode

import mysql.connector
from mysql.connector import errorcode

#Bastion of the Forebearers
try:
	cnx = mysql.connector.connect(user='root',password='password',database='players')
	cursor = cnx.cursor(buffered=True)
	while True:
		command = raw_input("~:")
		if command == "simulate":
			players = player_selector.player_selector(2575, 'silver')
			for x in range(0,10):
				print players[x][1]		
			
			
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
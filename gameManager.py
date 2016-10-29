import mysql.connector
from mysql.connector import errorcode
import random


try:
	cnx = mysql.connector.connect(user='root',password='password',database='players')
	cursor = cnx.cursor()
	
	user = raw_input("Please Enter Your Username: ")
	pword = raw_input("Please Enter Your Password: ")
	
	query = ('SELECT * FROM gold WHERE username="' + user + '" AND password="' + pword + '"')
	cursor.execute(query)
	
def MatchMaker(playerid,league):
	Ingame=[None]*10
	if(league=='gold'):
		available=("SELECT player_id FROM online_players WHERE league='gold' and player_id != %s")
		cursor.execute(available, (playerid))
		results = cursor.fetchall()
		for x in range(0,10):
			i= random.choice(results)
			results.remove(i)
			Ingame.append(i)

	else if(league =='silver'):
		available=("SELECT player_id FROM online_players WHERE league='silver' and player_id != %s")
		cursor.execute(available, (playerid))
		results = cursor.fetchall()
		for x in range(0,10):
			i= random.choice(results)
			results.remove(i)
			Ingame.append(i)

	else:
		available=("SELECT player_id FROM online_players WHERE league='bronze' and player_id != %s")
		cursor.execute(available, (playerid))
		results = cursor.fetchall()
		for x in range(0,10):
			i= random.choice(results)
			results.remove(i)
			Ingame.append(i)


def desideWinner():
	winner=random.randint(0,1)
	if( winner==0 ):
		print("Team one win!")
		
	else:
		print("Team two win!")


		
except mysql.connector.Error as err:
	if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
		print "Your username or password is incorrect"
	elif err.errno == errorcode.ER_BAD_DB_ERROR:
		print "Database does not exist"
	else:
		print err
else:
	cnx.close()
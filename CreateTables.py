import mysql.connector
import generate_name
import random
from mysql.connector import errorcode

DB_NAME = 'players'

TABLES = {}
TABLES['bronze'] = (
	"CREATE TABLE `bronze` ("
	"  `player_id` int(11) NOT NULL AUTO_INCREMENT,"
	"  `username` varchar(100) NOT NULL,"
	"  `password` varchar(25) NOT NULL,"
	"  `elo` int(4) NOT NULL,"
	"  `wins` int(10) NOT NULL,"
	"  `losses` int(10) NOT NULL,"
	"  `skill` int(2) NOT NULL,"
	"  `pref_role` enum('top','mid','bot','sup','jungle') NOT NULL,"
	"  PRIMARY KEY (`player_id`)"
	") ENGINE=InnoDB")
	
TABLES['silver'] = (
	"CREATE TABLE `silver` ("
	"  `player_id` int(11) NOT NULL AUTO_INCREMENT,"
	"  `username` varchar(100) NOT NULL,"
	"  `password` varchar(25) NOT NULL,"
	"  `elo` int(4) NOT NULL,"
	"  `wins` int(10) NOT NULL,"
	"  `losses` int(10) NOT NULL,"
	"  `skill` int(2) NOT NULL,"
	"  `pref_role` enum('top','mid','bot','sup','jungle') NOT NULL,"
	"  PRIMARY KEY (`player_id`)"
	") ENGINE=InnoDB")
	
	
TABLES['gold'] = (
	"CREATE TABLE `gold` ("
	"  `player_id` int(11) NOT NULL AUTO_INCREMENT,"
	"  `username` varchar(100) NOT NULL,"
	"  `password` varchar(25) NOT NULL,"
	"  `elo` int(4) NOT NULL,"
	"  `wins` int(10) NOT NULL,"
	"  `losses` int(10) NOT NULL,"
	"  `skill` int(2) NOT NULL,"
	"  `pref_role` enum('top','mid','bot','sup','jungle') NOT NULL,"
	"  PRIMARY KEY (`player_id`)"
	") ENGINE=InnoDB")
	
TABLES['online_players'] = (
	"CREATE TABLE `online_players` ("
	"  `player_id` int(11) NOT NULL,"
	"  `league` enum('gold', 'bronze', 'silver') NOT NULL,"
	"  `queued` int(2) NOT NULL,"
	"  PRIMARY KEY (`player_id`)"
	") ENGINE=InnoDB")
	
TABLES['in_game'] = (
	"CREATE TABLE `in_game` ("
	"  `player_id` int(11) NOT NULL,"
	"  `league` enum('gold', 'bronze', 'silver') NOT NULL,"
	"  PRIMARY KEY (`player_id`)"
	") ENGINE=InnoDB")

	
cnx = mysql.connector.connect(user='root',password='password')
cursor = cnx.cursor()

def create_database(cursor):
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except mysql.connector.Error as err:
        print "Failed creating database: {}".format(err)
        exit(1)

try:
    cnx.database = DB_NAME  
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        create_database(cursor)
        cnx.database = DB_NAME
    else:
        print(err)
        exit(1)
		
for name, ddl in TABLES.iteritems():
    try:
        print ("Creating table {}: ").format(name)
        cursor.execute(ddl)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print "already exists."
        else:
            print err.msg
    else:
        print "OK"
		
query = ('ALTER TABLE silver AUTO_INCREMENT=1001')
cursor.execute(query)

query = ('ALTER TABLE gold AUTO_INCREMENT=2001')
cursor.execute(query)

add_player = ("INSERT INTO gold "
			"(username, password, elo, wins, losses, skill, pref_role) "
			"VALUES (%s, %s, %s, %s, %s, %s, %s)")

for i in range(0,1000):
	role = random.randint(0,4)
	if role == 0:
		roleStr = 'top'
	elif role == 1:
		roleStr = 'bot'
	elif role == 2:
		roleStr = 'mid'
	elif role == 3:
		roleStr = 'sup'
	else:
		roleStr = 'jungle'
	data_player = (generate_name.generate_name(), 'password',random.randint(4000,6000), 0, 0, random.randint(0,10), roleStr)
	cursor.execute(add_player, data_player)
	
add_player = ("INSERT INTO silver "
			"(username, password, elo, wins, losses, skill, pref_role) "
			"VALUES (%s, %s, %s, %s, %s, %s, %s)")

for i in range(0,1000):
	role = random.randint(0,4)
	if role == 0:
		roleStr = 'top'
	elif role == 1:
		roleStr = 'bot'
	elif role == 2:
		roleStr = 'mid'
	elif role == 3:
		roleStr = 'sup'
	else:
		roleStr = 'jungle'
	data_player = (generate_name.generate_name(), 'password',random.randint(2000,4000), 0, 0, random.randint(0,10), roleStr)
	cursor.execute(add_player, data_player)
	
add_player = ("INSERT INTO bronze "
			"(username, password, elo, wins, losses, skill, pref_role) "
			"VALUES (%s, %s, %s, %s, %s, %s, %s)")

for i in range(0,1000):
	role = random.randint(0,4)
	if role == 0:
		roleStr = 'top'
	elif role == 1:
		roleStr = 'bot'
	elif role == 2:
		roleStr = 'mid'
	elif role == 3:
		roleStr = 'sup'
	else:
		roleStr = 'jungle'
	data_player = (generate_name.generate_name(), 'password',random.randint(0,2000), 0, 0, random.randint(0,10), roleStr)
	cursor.execute(add_player, data_player)

cnx.commit();			

cursor.close()
cnx.close()
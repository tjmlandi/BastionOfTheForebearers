import mysql.connector
import random
import os
import time
from mysql.connector import errorcode

#Bastion of the Forerunners
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
	
	#print "test"
	add_player = ("INSERT INTO online_players "
			"(player_id, league, queued) "
			"VALUES (%s, %s, %s)")
	data_player = (user[0], league, 0)
	#print "test2"
	cursor.execute(add_player, data_player)
	#print "test3"
	cnx.commit()
	#print "test4"
	
	os.system('cls') #clear screen
	while True:
		command = raw_input("~:")
		if command == "help":
			os.system('cls') #clear screen
			print "Available Commands: view_online, view_stats, queue"
			print "exit: Ends Program"
		elif command == "queue":
			os.system('cls') #clear screen
			
			#See if 10+ people are queued for a game
			count = 0
			cursor.execute("select * from online_players")
			results = cursor.fetchall()
			for row in results: #for each player queued
					count += 1
			if count < 10:
				print "Sorry, there are less than 10 players online"
				continue
			searching = True
			search_attempts = 0 #used to determine if there are even 10 queued players after attempting 100 times (elo deviation of 1000)
			user_elo = user[3] #logged in user's elo (for matchmaking range)
			queued_users_list = [] #list for game (10 players
			queued_users_list.append(user)
			user_elo_deviation = 10 # This number is the starting +- range for matchmaking
			
			#Update the user in online_players to show they are queued
			#print "TEST0"
			cursor.execute("UPDATE online_players SET queued=1 WHERE " +str(user[0])+ " = online_players.player_id")
			cnx.commit()
			#print "TEST1"
			
			while searching:
				#clear screen (for screen image)
				os.system('cls')
				if search_attempts == 100:
					print "Queueing was unsuccessful due to a lack of players online and queued within your ELO range."
					break
				search_attempts += 1
				#check if user is in a game already
				#print "TEST2"
				cursor.execute("SELECT * FROM in_game WHERE in_game.player_id = " +str(user[0]))
				data=cursor.fetchall()
				if len(data)!=0:
					cursor.execute("UPDATE online_players SET queued=0 WHERE " +str(user[0])+ "=online_players.player_id")
					cnx.commit()
					break
					
				#cursor.execute("IF EXISTS (SELECT * FROM in_game WHERE in_game.player_id = " +str(user[0])+ ")")
				
				#IF EXISTS (SELECT * FROM Products WHERE id = ?)
				#BEGIN
				#--do what you need if exists
				#END
				#ELSE
				#BEGIN
				#--do what needs to be done if not
				#END
				
				#print "TEST3"
				#results = cursor.fetchall()
				#if results == True:
				#	cursor.execute("UPDATE online_players SET queued=0 WHERE " +str(user[0])+ "=online_players.player_id")
				#	cnx.commit()
				#	break
				
				print ". . ."
				
				#select all players queued
				cursor.execute("select * from online_players where online_players.queued=1")
				results = cursor.fetchall()
				for row in results: #for each player queued
					league = row[1] #save what league they are in
					if league == 'gold':
						#select the players in the league that are queued(all their information, not just from online player columns)
						cursor.execute("select * from gold, online_players where gold.player_id = online_players.player_id and online_players.league = 'gold' and online_players.queued = 1")
						results = cursor.fetchall()
						#for each player check their elo if it is in range, if so, add to list
						for p_layer in results:
							if (p_layer[3] > (user_elo - user_elo_deviation)) and (p_layer[3] < (user_elo + user_elo_deviation)): #see if player is within elo range
								if (p_layer not in queued_users_list) and (len(queued_users_list) != 10):
									queued_users_list.append(p_layer)
					elif league == 'silver':
						cursor.execute("select * from silver, online_players where silver.player_id = online_players.player_id and online_players.league = 'silver' and online_players.queued = 1")
						results = cursor.fetchall()
						for p_layer2 in results:
							if (p_layer2[3] > (user_elo - user_elo_deviation)) and (p_layer2[3] < (user_elo + user_elo_deviation)): #see if player is within elo range
								if (p_layer2 not in queued_users_list) and (len(queued_users_list) != 10):
									queued_users_list.append(p_layer2)
					elif league == 'bronze':
						cursor.execute("select * from bronze, online_players where bronze.player_id = online_players.player_id and online_players.league = 'bronze' and online_players.queued = 1")
						results = cursor.fetchall()
						for p_layer3 in results:
							if (p_layer3[3] > (user_elo - user_elo_deviation)) and (p_layer3[3] < (user_elo + user_elo_deviation)): #see if player is within elo range
								if (p_layer3 not in queued_users_list) and (len(queued_users_list) != 10):
									queued_users_list.append(p_layer3)
				#for each person in the queue list (10 player list)
				for person in queued_users_list:
				
					#check if they are in a game already
					cursor.execute("SELECT * FROM in_game WHERE in_game.player_id = " +str(person[0]))
					data=cursor.fetchall()
					if len(data)!=0:
						queued_users_list.remove(person)
						break
						
					#cursor.execute('IF EXISTS (SELECT * FROM in_game WHERE in_game.player_id = "' +str(person[0])+ '")')
					#results = cursor.fetchall()
					
					#if they are in game, remove from list
					if results == True:
						queued_users_list.remove(person)
				time.sleep(3) #wait for any update/other queues
				os.system('cls')
				print ". ."
				time.sleep(3) #wait for any update/other queues
				user_elo_deviation = user_elo_deviation + 10 #increase elo range for search
				if len(queued_users_list) == 10:
					searching = False
				elif len(queued_users_list) > 10: #error check, queued_users_list has more than 10 people!
					print "ERROR: List has more than 10 people in it"
			
			#ADD PLAYERS TO IN_GAME
			os.system('cls')
			print "Starting Game..."
			add_player = ("INSERT INTO in_game "
			"(player_id, league) "
			"VALUES (%s, %s)")
			data_player = (user[0], league)
			cursor.execute(add_player, data_player)
			cnx.commit()
			
			#CHANGE ONLINE STATUS TO NOT QUEUED
			cursor.execute('UPDATE online_players SET queued=0 WHERE "' +str(user[0])+ '"=online_players.player_id')
			cnx.commit()
			
			#RUN GAME AND UPDATE ELO/ETC
			print "Game in Progess!"
			first_team_skill = 0
			first_team_elo = 0
			second_team_skill = 0
			second_team_elo = 0
			for user in queued_users_list[0:5]:
				first_team_skill += int(user[6])
				first_team_elo += int(user[3])
			for user2 in queued_users_list[5:]:
				second_team_skill += int(user2[6])
				second_team_elo += int(user2[3])
			difference_skill = abs(second_team_skill - first_team_skill)
			difference_skill += 50
			difference_elo = abs((second_team_elo - first_team_elo))/6
			randomint = random.randint(0,100)
			if (randomint > difference_skill) and (first_team_skill > second_team_skill):
				print "Your Team Won!"
				for user in queued_users_list[0:5]:
					cursor.execute("UPDATE bronze, silver, gold "
					"SET wins=wins+1 elo=elo+"+str(difference_elo)+""
					"WHERE " +str(user[0])+ "=bronze.player_id OR "
					"WHERE " +str(user[0])+ "=silver.player_id OR "
					"WHERE " +str(user[0])+ "=gold.player_id")
				cnx.commit()
				for user2 in queued_users_list[5:]:
					cursor.execute('UPDATE bronze, silver, gold SET losses=losses+1 elo=elo-"'+str(difference_elo)+'" WHERE "' +str(user2[0])+ '"=bronze.player_id OR "' +str(user[0])+ '"=silver.player_id OR "' +str(user[0])+ '"=gold.player_id')
				cnx.commit()
			if (randomint > difference_skill) and (first_team_skill < second_team_skill):
				print "Your Team Lost"
				for user in queued_users_list[0:5]:
					cursor.execute('UPDATE bronze, silver, gold SET losses=losses+1 elo=elo-"'+str(difference_elo)+'" WHERE "' +str(user[0])+ '"=bronze.player_id OR "' +str(user[0])+ '"=silver.player_id OR "' +str(user[0])+ '"=gold.player_id')
				cnx.commit()
				for user2 in queued_users_list[5:]:
					cursor.execute('UPDATE bronze, silver, gold SET wins=wins+1 elo=elo+"'+str(difference_elo)+'" WHERE "' +str(user2[0])+ '"=bronze.player_id OR "' +str(user[0])+ '"=silver.player_id OR "' +str(user[0])+ '"=gold.player_id')
				cnx.commit()
			if (randomint < difference_skill) and (first_team_skill < second_team_skill):
				print "Your Team Won!"
				for user in queued_users_list[0:5]:
					cursor.execute('UPDATE bronze, silver, gold SET wins=wins+1 elo=elo+"'+str(difference_elo)+'" WHERE "' +str(user[0])+ '"=bronze.player_id OR "' +str(user[0])+ '"=silver.player_id OR "' +str(user[0])+ '"=gold.player_id')
				cnx.commit()
				for user2 in queued_users_list[5:]:
					cursor.execute('UPDATE bronze, silver, gold SET losses=losses+1 elo=elo-"'+str(difference_elo)+'" WHERE "' +str(user2[0])+ '"=bronze.player_id OR "' +str(user[0])+ '"=silver.player_id OR "' +str(user[0])+ '"=gold.player_id')
				cnx.commit()
			if (randomint < difference_skill) and (first_team_skill > second_team_skill):
				print "Your Team Lost"
				for user in queued_users_list[0:5]:
					cursor.execute('UPDATE bronze, silver, gold SET losses=losses+1 elo=elo-"'+str(difference_elo)+'" WHERE "' +str(user[0])+ '"=bronze.player_id OR "' +str(user[0])+ '"=silver.player_id OR "' +str(user[0])+ '"=gold.player_id')
				cnx.commit()
				for user2 in queued_users_list[5:]:
					cursor.execute('UPDATE bronze, silver, gold SET wins=wins+1 elo=elo+"'+str(difference_elo)+'" WHERE "' +str(user2[0])+ '"=bronze.player_id OR "' +str(user[0])+ '"=silver.player_id OR "' +str(user[0])+ '"=gold.player_id')
				cnx.commit()
			time.sleep(5)
			continue
				
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
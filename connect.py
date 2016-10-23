import mysql.connector
from mysql.connector import errorcode

try:
  cnx = mysql.connector.connect(user='root',password='password',database='sakila')
  cursor = cnx.cursor()
  
  query = ("SELECT actor_id, first_name FROM actor")
  
  cursor.execute(query)
  
  for (first_name) in cursor:
	print first_name
  
  
except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with your user name or password")
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database does not exist")
  else:
    print(err)
else:
  cnx.close()
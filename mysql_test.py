import mysql
from datetime import datetime
import mysql.connector

db = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    passwd = 'fjfj',
    database = 'testdatabase'
    )
mycursor = db.cursor()

# mycursor.execute('CREATE DATABASE testdatabase')

# mycursor.execute('CREATE TABLE Person (name VARCHAR(50), age smallint UNSIGNED, personID int PRIMARY KEY AUTO_INCREMENT)')

# mycursor.execute('DESCRIBE Person')

# mycursor.execute('INSERT INTO Person (name, age) VALUES (%s, %s)', ('Tim', 19))
mycursor.execute('INSERT INTO Person (name, age) VALUES (%s, %s)', ('Joe', 21))
# db.commit()
# mycursor.execute()
# for x in mycursor:
#     print(x)
mycursor.execute('SELECT * FROM Person')
for x in mycursor:
    print(x)

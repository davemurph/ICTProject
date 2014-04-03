# script to initialise database

import sqlite3

connection = sqlite3.connect('test.db')

cursor = connection.cursor()

cursor.execute('''CREATE TABLE Users
					(UserID INTEGER PRIMARY KEY AUTOINCREMENT,
						email VARCHAR(120) NOT NULL UNIQUE,
						pwdhash VARCHAR(120) NOT NULL)''')

connection.commit()

connection.close()
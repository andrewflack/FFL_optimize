# -*- coding: utf-8 -*-
"""
Created on Fri Aug 14 18:28:51 2015

Author: Andrew
"""

# CREATE AND POPULATE DATABASE

import sqlite3
import csv

myConnection = sqlite3.connect('FFL_optimal_draft.db')
myCursor = myConnection.cursor()

### Create player_info table
sqlString = """
            CREATE TABLE IF NOT EXISTS player_info
            (name char,
             rank int,
             tier int,
             pos char,
             team char,
             bye_week int,
             best_rank int,
             worst_rank int,
             avg_rank num,
             rank_std num,
             adp int,
             PPG num,
             risk num,
             standard_risk num);
             """

myCursor.execute(sqlString)

### Populate player_info table
myFile = open('player_info.csv', 'rt')
myReader = csv.reader(myFile)

player = []
for row in myReader:
	player.append((row[0].strip(), row[1].strip(), row[2].strip(), row[3].strip(), row[4].strip(), row[5].strip(), row[6].strip(), row[7].strip(), row[8].strip(), row[9].strip(), row[10].strip(), row[11].strip(), row[12].strip(), row[13].strip()))
myFile.close()

myCursor.execute("DELETE FROM player_info")
myCursor.executemany("INSERT INTO player_info VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", player)

### Create hist_costs table
sqlString = """
	CREATE TABLE IF NOT EXISTS hist_costs
	(pos char,
	tier int,
	cost int);
	"""
myCursor.execute(sqlString)

### Populate hist_costs table
myFile = open('hist_costs.csv', 'rt')
myReader = csv.reader(myFile)

cost_entry = []
for row in myReader:
	cost_entry.append((row[0].strip(), row[1].strip(), row[2].strip()))
myFile.close()

myCursor.execute("DELETE FROM hist_costs")
myCursor.executemany("INSERT INTO hist_costs VALUES(?, ?, ?)", cost_entry)

myCursor.execute(sqlString)

### Commit all changes to the database
myConnection.commit()

### Close the cursor and connection
myCursor.close()
myConnection.close()
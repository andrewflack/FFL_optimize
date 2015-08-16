# -*- coding: utf-8 -*-
"""
Created on Fri Aug 14 18:38:06 2015

Author: Andrew
"""

import sqlite3
import numpy as np

myConnection = sqlite3.connect('FFL_optimal_draft.db')
myCursor = myConnection.cursor()

# cost: dictionary in dictionary

sqlString = """
	SELECT pos, tier, cost
	FROM hist_costs
	"""

myCursor.execute(sqlString)

b = myCursor.fetchall()

#for row in b:
# print row[0], row[1], row[2]
#
#print '\n\n'

cost = {}
for row in b:
    if row[0] not in cost:
        cost[row[0]] = []
    cost[row[0]].append(row[2])

#print(cost)

# PPG: dictionary in dictionary

sqlString = """
            SELECT pos, tier, PPG
            FROM player_info
            """

myCursor.execute(sqlString)

b = myCursor.fetchall()

#for row in b:
# print row[0], row[1], row[2]
#
#print '\n\n'

PPG = {}
for row in b:
    if row[0] not in PPG:
        PPG[row[0]] = {}
    if row[1] not in PPG[row[0]]:
        PPG[row[0]][row[1]] = []
    PPG[row[0]][row[1]].append(row[2])
    
for p in PPG:
    for t in range(1,21):
        if t not in PPG[p]:
            PPG[p][t] = 0
        PPG[p][t] = np.mean(PPG[p][t])

# count: dictionary in dictionary

sqlString = """
            SELECT pos, tier
            FROM player_info
            """

myCursor.execute(sqlString)
b = myCursor.fetchall()

tmp = {}
for row in b:
    if row[0] not in tmp:
        tmp[row[0]] = []
    tmp[row[0]].append(row[1])

count = {}
for p in tmp:
    if p not in count:
        count[p] = {}
    for t in range(1,21):
        if t not in count[p]:
            count[p][t] = 0
        count[p][t] = tmp[p].count(t)

# risk: dictionary in dictionary

pos = ['QB', 'RB', 'WR', 'TE', 'DST', 'K']
tiers = range(1,21)

budget = 200
maxQBs = 2
maxDSTs = 1
maxKs = 1
maxTEs = 1

myCursor.close()
myConnection.close()
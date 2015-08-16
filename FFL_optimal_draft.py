# -*- coding: utf-8 -*-
"""
Created on Fri Aug 14 18:50:43 2015

Author: Andrew
"""

from gurobipy import *
from build_FFL_data_structures import *

# Create a model object that will contain the variables and constraints of the LP formulation
FFL = Model()

# Set the model sense and update
FFL.modelSense = GRB.MAXIMIZE
FFL.update()

# Create the variables
x = {}

for p in pos:
	for t in tiers:
		x[p,t] = FFL.addVar(obj = 1, vtype = GRB.INTEGER, name = 'x_' + p + '_' + str(t))

FFL.update()

# Create a dictionary to hold contraints
myConsts = {}

# 1 - Must draft 13 players
constrName = 'Draft13'
myConsts[constrName] = FFL.addConstr(quicksum(x[p,t] for p in pos for t in tiers) == 13, name = constrName)

FFL.update()

# 2 - Must stay below max budget ($200)
constrName = 'UnderBudget'
myConsts[constrName] = FFL.addConstr(quicksum((cost[p][t-1])*x[p,t] for p in pos for t in tiers) <= budget, name = constrName)

FFL.update()

#3 - Must have at least 1 K
constrName = 'AtLeastOneK'
myConsts[constrName] = FFL.addConstr(quicksum(x['K',t] for t in tiers) >= 1, name = constrName)

FFL.update()

#4 - Must have at least 1 DST
constrName = 'AtLeastOneDST'
myConsts[constrName] = FFL.addConstr(quicksum(x['DST',t] for t in tiers) >= 1, name = constrName)

FFL.update()

#5 - Must have at least 1 QB
constrName = 'AtLeastOneQB'
myConsts[constrName] = FFL.addConstr(quicksum(x['QB',t] for t in tiers) >= 1, name = constrName)

FFL.update()

#6 - Must have at least 2 RB
constrName = 'AtLeastTwoRB'
myConsts[constrName] = FFL.addConstr(quicksum(x['RB',t] for t in tiers) >= 2, name = constrName)

FFL.update()

#7 - No More than MaxQBs
constrName = 'NoMoreThanMaxQBs'
myConsts[constrName] = FFL.addConstr(quicksum(x['QB',t] for t in tiers) <= maxQBs, name = constrName)

FFL.update()

#8 - No More than MaxDSTs
constrName = 'NoMoreThanMaxDSTs'
myConsts[constrName] = FFL.addConstr(quicksum(x['DST',t] for t in tiers) <= maxDSTs, name = constrName)

FFL.update()

#9 - No More than MaxKs
constrName = 'NoMoreThanMaxKs'
myConsts[constrName] = FFL.addConstr(quicksum(x['K',t] for t in tiers) <= maxKs, name = constrName)

FFL.update()

#9 - No More than MaxTEs
constrName = 'NoMoreThanMaxTEs'
myConsts[constrName] = FFL.addConstr(quicksum(x['TE',t] for t in tiers) <= maxKs, name = constrName)

FFL.update()

#10 - No More than 8 WRs
constrName = 'NoMoreThanEightWRs'
myConsts[constrName] = FFL.addConstr(quicksum(x['WR',t] for t in tiers) <= 8, name = constrName)

FFL.update()

#11 - No More than 8 RBs
constrName = 'NoMoreThanEightRBs'
myConsts[constrName] = FFL.addConstr(quicksum(x['RB',t] for t in tiers) <= 8, name = constrName)

FFL.update()

#12 - Cannot draft more from a tier than are available in that tier
for p in pos:
    for t in tiers:
        constrName = 'NoMoreThanAvailableInTier_' + p + '_' + str(t)
        myConsts[constrName] = FFL.addConstr(x[p,t] <= count[p][t], name = constrName)

FFL.update()

### END CONSTRAINTS ###

# Write the LP file
FFL.write('FFL.lp')

# Set parameters
FFL.setParam('SolutionLimit',1)
FFL.setParam('MIPFocus',1)

# Solve the optimization model
FFL.optimize()

# Extract the solution
FFL.write('NFL_sched.sol')

# Print scheduled games with scores
print('')
print('pos','tier','quantity','cost')
for p in pos:
    for t in tiers:
	if x[p,t].x > 0.5:
         print p, t, x[p,t].x, (cost[p][t-1])*x[p,t].x
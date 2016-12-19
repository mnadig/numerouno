# PuLP documentation : https://pythonhosted.org/PuLP/CaseStudies/a_blending_problem.html

# Version 2 : Manage variables using dictionaries

from pulp import *

ndays = 45.0 # Days invested
amount = 3200.0 # Amount invested
max_percentage_of_portfolio = 45.0

print "# of days invested = ", ndays
print "Investment amount = ", amount
print "Max % of portfolio per scrip = ", max_percentage_of_portfolio
print "-----"


# i is the scrip
price = {'SINO': 1.2, 'AAPL': 100.0, 'FSAM': 5.9}
scrips = price.keys()
change = {'SINO': 0.2, 'AAPL': 1.01, 'FSAM': 0.4}
days = {'SINO': 5.0, 'AAPL': 30.0, 'FSAM': 15.0}


# Create the 'prob' variable to contain the problem data
prob = LpProblem("Portfolio Gain Prediction", LpMaximize)


# A dictionary called volume_vars is created to contain the referenced Variables
volume_vars = LpVariable.dicts("n", scrips, lowBound=0, cat=LpInteger)


# The objective function is added to 'prob' first
# Objective : Maximize gain_percent
# gain_per_day = ndays / amount * 100 * sum ( c_i / d_i)
m_const = ndays / amount * 100.0
gain_per_day = {k : m_const * v / days[k] for k, v in change.items()}
prob += lpSum([gain_per_day[i] * volume_vars[i] for i in scrips]), "Expected gain %"


# Constraint on investment in portfolio
# sum ( p_i * a_i ) == amount
prob += lpSum([price[i] * volume_vars[i] for i in scrips]) <= amount, "Investment in portfolio"


# Constraints on percentage of portfolio that can be invested in scrip i
for i in scrips:
    prob += price[i] * volume_vars[i] <= max_percentage_of_portfolio / 100 * amount


prob.writeLP("GainPrediction.lp")

prob.solve()

prob_vars = prob.variables()

# Each of the variables is printed with it's resolved optimum value
for v in prob.variables():
    print v.name, "=",  v.varValue


# The optimised objective function value is printed to the screen
print "Expected gain % = ", value(prob.objective)
print "Value of investment", sum([price[k] * v.value() for k, v in volume_vars.items()])
print "------"

# print prob

print "Picture abhi baaki hain mere dost ...."






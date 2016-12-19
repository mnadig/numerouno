# PuLP documentation : https://pythonhosted.org/PuLP/CaseStudies/a_blending_problem.html

# Version 1 : Manage variables individually

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
change = {'SINO': 0.2, 'AAPL': 1.01, 'FSAM': 0.4}
days = {'SINO': 5.0, 'AAPL': 30.0, 'FSAM': 15.0}


prob = LpProblem("Portfolio Gain Prediction", LpMaximize)

# a_i == # of shares of scrip i
a_1 = LpVariable("nSINO", 0, None, LpInteger)
a_2 = LpVariable("nAAPL", 0, None, LpInteger)
a_3 = LpVariable("nFSAM", 0, None, LpInteger)


# Objective problem : Maximize gain_percent
# gain_per_day = ndays / amount * 100 * sum ( c_i / d_i)
m_const = ndays / amount * 100
gain_per_day = {k : m_const * v / days[k] for k, v in change.items()}
prob += gain_per_day['SINO'] * a_1 + gain_per_day['AAPL'] * a_2 + gain_per_day['FSAM'] * a_3, \
        "Expected gain"


# Constraint on value of portfolio
# sum ( p_i * a_i ) == amount
prob += price['SINO'] * a_1 + price['AAPL'] * a_2 + price['FSAM'] * a_3 <= 3200, \
        "Investment in portfolio"


# Constraints on percentage of portfolio that can be invested in scrip i
prob += price['SINO'] * a_1 <= max_percentage_of_portfolio / 100 * amount
prob += price['AAPL'] * a_2 <= max_percentage_of_portfolio / 100 * amount
prob += price['FSAM'] * a_3 <= max_percentage_of_portfolio / 100 * amount





prob.writeLP("GainPrediction.lp")

prob.solve()

prob_vars = prob.variables()

# Each of the variables is printed with it's resolved optimum value
for v in prob.variables():
    print v.name, "=",  v.varValue


# The optimised objective function value is printed to the screen
print "Expected gain % = ", value(prob.objective)

print "Value of investment = ", price['SINO'] * a_1.value() + price['AAPL'] * a_2.value() + \
                                price['FSAM'] * a_3.value()
print "------"

# print prob

print "Picture abhi baaki hain mere dost ...."






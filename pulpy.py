# Version 3 : Simulation

from datetime import datetime, timedelta
from pulp import LpProblem, LpMaximize, LpVariable, LpInteger, lpSum, value


def get_portfolio_stats(lots):
    stats = dict()
    for lot in lots:
        scrip, n, price, buy_date = lot
        buy_date = datetime.strptime(buy_date, '%Y-%m-%d')

        cost = float(n) * float(price)
        vol = n
        min_cost_price = price
        max_cost_price = price
        oldest_lot_date = buy_date

        if stats.has_key(scrip):
            record = stats[scrip]
            cost += record[0]
            vol += record[1]
            min_cost_price = min(min_cost_price, record[2])
            max_cost_price = max(max_cost_price, record[3])
            if oldest_lot_date > buy_date:
                oldest_lot_date = buy_date

        stats[scrip] = (cost, vol, min_cost_price, max_cost_price, oldest_lot_date)
    return stats


def sell(existing_portfolio, mkt_prices, config):
    _sold_lots = []
    _profit = 0.0
    _held_lots = []

    date_format_str = config['date_format_str']
    max_days_hold = config['max_days_hold']
    min_gain_pct = config['min_gain_pct']
    depository_fee = config['depository_fee']

    sell_date = datetime.now().strftime(date_format_str)
    print "Today : ", sell_date

    oldest_permitted_date = datetime.now() - timedelta(days=max_days_hold)
    print "Selling lots bought before", oldest_permitted_date.strftime(date_format_str)

    for _lot in existing_portfolio:
        scrip, n, costprice, buy_date = _lot

        mkt_price, open, high, low = mkt_prices[scrip]

        # Sell lots satisfying these criteria:
        # 1. Held longer than max_days_old
        # 2. Gained at least min_gain_pct
        if oldest_permitted_date > datetime.strptime(buy_date, date_format_str)\
                or mkt_price >= (min_gain_pct / 100 * costprice):
            _proceeds = mkt_price * n - depository_fee
            _txn_profit = _proceeds - (n * costprice)
            print "Sold %d shares of %s @ price %.2f with profit/loss of %.2f, txn value = %.2f" \
                  % (n, scrip, mkt_price, _txn_profit, _proceeds)
            _sold_lots.append((scrip, n, costprice, buy_date, mkt_price, depository_fee, sell_date))
            _profit += _txn_profit
        else:
            _held_lots.append(_lot)

    return _held_lots, _sold_lots, _profit


def get_market_info(day):
    prices = [
        {'SINO': (0.88, 0.9, 0.9, 0.88), 'FSAM': (6.7, 6.7, 6.7, 6.2), 'AAPL': (100, 101, 105, 99)},
        {'SINO': (1.20, 1.3, 1.45, 1.2), 'FSAM': (5.8, 5.8, 5.8, 5.8), 'AAPL': (101, 99, 101, 99)},
        {'SINO': (0.75, 0.7, 0.75, 0.7), 'FSAM': (5.8, 5.8, 5.8, 5.8), 'AAPL': (101, 99, 101, 99)}]
    return prices[day]


def get_buy_recommendations(day, held_lots, mkt_prices, sold_lots, config):
    recommendations = dict()

    portfolio_stats = get_portfolio_stats(held_lots)

    investment_in_stocks = sum([rec[0] for rec in portfolio_stats.values()])

    investment_at_day_open = config['investment_at_day_open'][day]
    cash_available = investment_at_day_open - investment_in_stocks

    print "Current Share of portfolio"
    print {scrip: rec[0]/investment_at_day_open*100 for scrip, rec in portfolio_stats.items()}

    print "Amount invested : ", investment_in_stocks
    print "Amount available for investing : ", cash_available

    # Calculate change as high - low
    sold_scrips = frozenset([ lot[0] for lot in sold_lots ])
    print "sold scrips", sold_scrips
    change = {scrip: rec[2]-rec[3] for scrip, rec in mkt_prices.items()
              if scrip not in sold_scrips}
    print "change", change

    scrips = change.keys()
    print "scrips", scrips

    # Create the 'prob' variable to contain the problem data
    prob = LpProblem("Portfolio Gain Prediction", LpMaximize)

    # A dictionary called volume_vars is created to contain the referenced Variables
    volume_vars = LpVariable.dicts("n", scrips, lowBound=0, cat=LpInteger)

    # The objective function is added to 'prob' first
    #  Objective : Maximize gain
    prob += lpSum(change[i] * volume_vars[i] for i in scrips), "Expected gain"

    # Constraint on cost of purchases
    #  sum ( p_i * a_i ) <= cash_available
    prob += lpSum([mkt_prices[i][0] * volume_vars[i] for i in scrips]) <= cash_available, \
            "Cost of purchases"

    # Constraints on percentage of portfolio that can be invested in scrip i
    max_percentage_of_portfolio = config['max_percentage_of_portfolio']
    for i in scrips:
        existing_investment = 0.0
        if portfolio_stats.has_key(i):
            existing_investment = portfolio_stats[i][0]
        max_inv = (max_percentage_of_portfolio / 100 * investment_at_day_open) - existing_investment
        prob += mkt_prices[i][0] * volume_vars[i] <= max_inv
        print "Max investment permitted for %s : %0.2f" % (i, max_inv)

    prob.writeLP("GainPrediction.lp")

    prob.solve()

    for scrip, v in volume_vars.items():
        n = int(v.varValue)
        if n > 0 :
            recommendations[scrip] = (n, mkt_prices[scrip][0])

    print "purchase recommendations : ", recommendations

    # The optimised objective function value is printed to the screen
    print "Expected gain  = ", value(prob.objective)
    print "Value of investment", \
        sum([v[0] * v[1] for k, v in recommendations.items()])

    return recommendations


# TODO : Simulate purchases based on recos and update portfolio
def buy(day, held_lots, mkt_prices, sold_lots, config):
    new_portfolio = []

    recommendations = get_buy_recommendations(day, held_lots, mkt_prices, sold_lots, config)

    return new_portfolio


def trade(config, day):
    print "Trading Day : ", day

    portfolio = config['portfolio_lots_at_day_open'][day]

    # print_portfolio_stats(portfolio, day, config)

    mkt_prices = get_market_info(day)

    # Sell first
    held_lots, sold_lots, profit = sell(portfolio, mkt_prices, config)

    # Buy, assuming no day-trades allowed
    new_portfolio = buy(day, held_lots, mkt_prices, sold_lots, config)
    return new_portfolio


# TODO : Run simulation over multiple days
def main():
    config = dict(
        n_days = 1,
        init_amount = 3200.0,
        max_percentage_of_portfolio = 33.33,
        min_gain_pct = 2,
        max_days_hold = 180,
        depository_fee = 0.03,
        date_format_str='%Y-%m-%d',
        deposit_at_day_open = [0],
        withdrawal_at_day_open = [0],
        portfolio_lots_at_day_open = [list()]
    )
    config['investment_at_day_open'] = [config['init_amount']]
    # config['portfolio_lots_at_day_open'] = [[('SINO', 100, 0.5, '2016-12-01'),
    #                                          ('SINO', 50, 1, '2016-01-01'),
    #                                          ('AAPL', 1, 105, '2016-09-01')]]

    print "# of days in simulation = ", config['n_days']
    print "Initial investment amount = ", config['init_amount']
    print "Max % of portfolio per scrip = ", config['max_percentage_of_portfolio']
    print "Minimum gain % for sale = ", config['min_gain_pct']
    print "Max days to hold lots = ", config['max_days_hold']
    print "Depository Fee per transaction = ", config['depository_fee']
    print "-----"

    for day in range(config['n_days']):
        new_portfolio = trade(config, day)
        config['portfolio_lots_at_day_open'].append(new_portfolio)


main()
print "\n\n\nPicture abhi baaki hain mere dost ...."

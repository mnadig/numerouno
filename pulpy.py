# Version 3 : Simulation

from datetime import datetime, timedelta

def get_portfolio_metrics(lots):
    _cost = dict()
    _vol = dict()
    _min_cost_price = dict()
    _oldest_lot_date = dict()
    for lot in lots:
        scrip, n, price, buy_date = lot
        buy_date = datetime.strptime(buy_date, '%Y-%m-%d')
        if not _cost.has_key(scrip):
            _cost[scrip] = 0.0
            _vol[scrip] = 0
            _min_cost_price[scrip] = price
            _oldest_lot_date[scrip] = buy_date
        _cost[scrip] += float(n) * float(price)
        _vol[scrip] += n
        if _min_cost_price[scrip] > price:
            _min_cost_price[scrip] = price
        if _oldest_lot_date[scrip] > buy_date:
            _oldest_lot_date[scrip] = buy_date
    return _cost, _vol, _min_cost_price, _oldest_lot_date


def get_market_info(day):
    prices = [{'SINO': 0.88, 'FSAM': 6.7, 'AAPL': 100},
              {'SINO': 1.20, 'FSAM': 5.8, 'AAPL': 101},
              {'SINO': 0.75, 'FSAM': 5.9, 'AAPL': 95}]
    return prices[day]


def sell(existing_portfolio, mkt_prices, min_gain_pct, max_days_hold, depository_fee,
         date_format_str='%Y-%m-%d'):
    _sold_lots = []
    _profit = 0.0
    _held_lots = []

    sell_date = datetime.now().strftime(date_format_str)
    print "Today : ", sell_date

    oldest_permitted_date = datetime.now() - timedelta(days=max_days_hold)
    print "Will sell all lots bought before ", oldest_permitted_date

    for _lot in existing_portfolio:
        scrip, n, costprice, buy_date = _lot

        mkt_price = mkt_prices[scrip]

        # Sell lots satisfying these criteria:
        # 1. Held longer than max_days_old
        # 2. Gained at least min_gain_pct
        if oldest_permitted_date > datetime.strptime(buy_date, date_format_str)\
                or mkt_price >= (min_gain_pct / 100 * costprice):
            _proceeds = mkt_price * n - depository_fee
            _txn_profit = _proceeds - (n * costprice)
            print "Sold %d shares of %s @ price %.2f with profit/loss of %.2f, txn value = %.2f" \
                  % (n, scrip, mkt_price, _txn_profit, _proceeds)
            sold_lots.append((scrip, n, costprice, buy_date, mkt_price, depository_fee, sell_date))
            _profit += _txn_profit
        else:
            _held_lots.append(_lot)

    return _held_lots, _sold_lots, _profit



n_days = 1
init_amount = 3200.0 # Amount invested
max_percentage_of_portfolio = 33.33
min_gain_pct = 2
max_days_hold = 180
depository_fee = 0.03

print "# of days in simulation = ", n_days
print "Initial investment amount = ", init_amount
print "Max % of portfolio per scrip = ", max_percentage_of_portfolio
print "Minimum gain % for sale = ", min_gain_pct
print "Max days to hold lots = ", max_days_hold
print "Depository Fee per transaction = ", depository_fee
print "-----"


investment_at_day_open = [init_amount]
deposit_at_day_open = [0]
withdrawal_at_day_open = [0]
portfolio_lots_at_day_open = [list()]
# portfolio_lots_at_day_open = [[('SINO', 100, 0.5, '2016-12-01'), ('SINO', 50, 1, '2016-01-01'),
#                                ('AAPL', 1, 105, '2016-09-01')]]



for day in range(n_days):
    print "Day ", day

    portfolio_lots_at_open = portfolio_lots_at_day_open[day]

    # cost, vol, min_cost_price, oldest_lot_date = get_portfolio_metrics(portfolio_lots_at_open)
    # print "cost", cost
    # print "vol", vol
    # print "min_cost_price", min_cost_price
    # print "oldest_lot_date", oldest_lot_date
    #
    # investment_in_stocks = sum([c for c in cost.values()])
    # print "Amount invested : ", investment_in_stocks
    #
    # cash_available = investment_at_day_open[day] - investment_in_stocks
    # print "Amount available for investing : ", cash_available
    #
    # print "Current Share of portfolio"
    # print {k : v/(investment_at_day_open[day])*100 for k,v in cost.items()}

    prices_now = get_market_info(day)
    held_lots, sold_lots, profit = sell(portfolio_lots_at_open, prices_now, min_gain_pct,
                                        max_days_hold, depository_fee)

    portfolio_lots_at_day_open.append(held_lots)


print "\n\n\nPicture abhi baaki hain mere dost ...."

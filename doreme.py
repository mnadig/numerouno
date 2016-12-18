import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Display all columns on one line
pd.set_option('display.line_width', 2000)
pd.set_option('display.max_columns', 20)


tradestsvfile = 'resources/sample-trades.tsv'

# index_col=0
# index_col=[0, 10, 11]
trades_df = pd.read_csv(tradestsvfile, delimiter='\t', skipinitialspace=True,
                        header=0, skiprows=[309, 337],
                        usecols=[1, 2, 5, 6, 8, 10, 11, 12, 15, 16, 18, 19, 20, 21],
                        names=['Name', 'Volume', 'Total cost', 'C.P.', 'Change',
                               'S.P.', 'Sale Fee', 'Proceeds', 'Gain', 'Gain%',
                               'Buy Date', 'Sell Date', 'Days Held', 'Annual%'],
                        dtype={'Name': str, 'Volume': np.uint16, 'Total cost': np.float16,
                               'C.P.': np.float16, 'Change': np.float16, 'S.P.': np.float16,
                               'Sale Fee': np.float16, 'Proceeds': np.float16, 'Gain': np.float16,
                               'Gain%': np.float16, 'Buy Date': object, 'Sell Date': object,
                               'Days Held': np.uint16, 'Annual%': np.float16},
                        parse_dates=['Buy Date', 'Sell Date'])
print trades_df[:10]

# Plot on graph
# trades_df['Gain'].plot()

print trades_df['Name'].value_counts()
print "----"


# Row filtering
gain_more_than_5_percent = trades_df['Gain%'] > 5.0
sold_within_15_days = trades_df['Days Held'] <= 15
print trades_df[gain_more_than_5_percent & sold_within_15_days]\
    [['Name', 'Gain', 'Gain%', 'Buy Date', 'Sell Date', 'Days Held']]
print "----"


print trades_df['Gain'].sum()


# Gain/Loss per stock
plot_data = trades_df[['Name', 'Gain']] \
    .groupby('Name') \
    .aggregate(sum) \
    .sort_values(['Gain'], ascending=False)

plot_data.plot(kind='bar')

print plot_data

print "Gain - Mean"
print trades_df['Gain'].mean()

print "Gain - Standard deviation"
print trades_df['Gain'].std()


# Identify outliers
def find_outliers(df, fieldName):
    return df[fieldName] - df[fieldName].mean() > 1.96*trades_df[fieldName].std()


trades_df['Gain Outlier'] = find_outliers(trades_df[trades_df['Gain'] > 0], 'Gain')
print "Gain Outlier trades"
print trades_df[trades_df['Gain Outlier']]
print "----"

# TODO : Fix this
# print trades_df[not np.isnan(trades_df['Gain']) & trades_df['Gain'] < 0]
# trades_df['Loss Outlier'] = find_outliers(trades_df[trades_df['Gain'] < 0], 'Gain')
# print "Loss Outlier trades"
# print trades_df[trades_df['Loss Outlier']]
# print "----"


trades_df['Days Held Outlier'] = find_outliers(trades_df, 'Days Held')
print "Days Held Outlier"
print trades_df[trades_df['Days Held Outlier']]
print "----"



# Needed to show the plots
plt.show()



print "Picture abhi baaki hai mere dost ... "

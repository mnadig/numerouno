import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

tradestsvfile = 'resources/sample-trades.tsv'

# index_col=0
# index_col=[0, 10, 11]
trades_df = pd.read_csv(tradestsvfile, delimiter='\t', skipinitialspace=True,
                        header=0, skiprows=[309, 337],
                        usecols=[1, 2, 5, 6, 8, 10, 11, 12, 15, 16, 18, 19, 20, 21],
                        names=['Name', 'Volume', 'Total cost', 'C.P.', 'Change',
                               'S.P.', 'Sale Fee', 'Proceeds', 'Gain', 'Gain%',
                               'Buy Date', 'Sell Date', 'Days', 'Annual%'],
                        dtype={'Name': str, 'Volume': np.uint16, 'Total cost': np.float16,
                               'C.P.': np.float16, 'Change': np.float16, 'S.P.': np.float16,
                               'Sale Fee': np.float16, 'Proceeds': np.float16, 'Gain': np.float16,
                               'Gain%': np.float16, 'Buy Date': object, 'Sell Date': object,
                               'Days': np.uint16, 'Annual%': np.float16},
                        parse_dates=['Buy Date', 'Sell Date'])
print trades_df[:10]

print trades_df['Name'].value_counts()


# # Plot on graph
# trades_df['Gain'].plot()
# plt.show()



print "Picture abhi baaki hai mere dost ... "

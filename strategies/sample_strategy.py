import pandas as pd
# import the backtest library
import optopsy as op

pd.options.display.width = None

# define the structure of our data, sourced from 'www.historicaloptiondata.com'
data_struct = (
    {'symbol', 0},
    {'underlying_price', 1},
    {'option_symbol', 3},
    {'option_type', 4},
    {'expiration', 5},
    {'quote_date', 6},
    {'strike', 7},
    {'bid', 9},
    {'ask', 10},
    {'volume', 11},
    {'oi', 12},
    {'iv', 14},
    {'delta', 17},
    {'gamma', 18},
    {'theta', 19},
    {'vega', 20}
)

# fetch the data
data = op.get('../data/A.csv', start='1/1/2016', end='12/31/2016', struct=data_struct)

strategy_1 = op.Strategy('Weekly Bull Put Spread', [
    op.algos.EntryAbsDelta(ideal=0.5, min=0.4, max=0.6),
    op.algos.EntrySpreadPrice(ideal=1.0),
    op.algos.EntryDaysToExpiration(ideal=47, min=40, max=52),
    op.algos.EntryDayOfWeek(ideal=4)
], op.options.LongPutSpread(data, width=2))

# Here we create another 'Strategy', one that is designed to hedge the strategy above
strategy_2 = op.Strategy('Weekly Bull Put Spread Strategy', [
    op.algos.EntryAbsDelta(ideal=0.2, min=0.4, max=0.6),
    op.algos.EntryDaysToExpiration(ideal=47, min=40, max=52),
    op.algos.EntryDayOfWeek(ideal=4)
], op.options.LongPut(data))


def run_strat():
    # Create an instance of Optopsy with strategy settings
    optopsy = op.Optopsy([strategy_1, strategy_2])

    # Set our desired cash start
    optopsy.set_cash(100000)

    # Print out the starting conditions
    print('Starting Portfolio Value: %.2f' % optopsy.get_value())

    # Run over everything
    optopsy.run()

    # Print out the final result
    print('Final Portfolio Value: %.2f' % optopsy.get_value())


if __name__ == '__main__':
    run_strat()

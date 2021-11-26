from .bs import BuySell

def static_backtest(strategy, capital=1000, max_share=1000):
    # Static Backtest from data
    bs = BuySell(capital=capital, max_share=max_share)
    data = strategy.data
    length = len(data)

    # Backtest 
    for i in range(length):
        # Skipping 1st day
        if i == 0:
            continue
        is_above = data['above'].iloc[i - 1]
        is_good_buy = data['Good-Buy'].iloc[i]
        buying_price = data['Low'].iloc[i]
        selling_pirce = data['Close'].iloc[i]
        high = data['High'].iloc[i]
        # Buy Sell Logic
        if i + 1 == length:
            # Selling at the last day
            if bs.is_holding:
                bs.sell(selling_pirce)
        else:
            # Check for Holding or not
            if not bs.is_holding:
                if is_above and is_good_buy:
                    bs.buy(buying_price)
            else:
                pct = high / bs.buy_at - 1
                good_sell = pct >= strategy.apct
                if not is_above or good_sell:
                    if good_sell:
                        bs.sell(high)
                    else:
                        bs.sell(selling_pirce)
    
    print('#####################################################')
    bs.show_results()
    print('#####################################################')
    avg_days_per_trade = length / bs.results['Num-Trades']
    stock_momentum = data['Close'].iloc[-1] / data['Close'].iloc[0] - 1
    print('Average days per trade: {:.2f}'.format(avg_days_per_trade))
    print("Stock's momemtum: {:.2f}".format(stock_momentum))
    print('#####################################################')
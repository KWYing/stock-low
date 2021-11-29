import numpy as np
import pandas as pd

class BuySell:
    def __init__(self, capital=None, max_share=None):
        self.original_capital = capital
        self.capital = capital
        self.max_share = max_share
        self.share = 0
        self.is_holding = False
        self.buy_at = 0
        # Array for dollar gain per trade 
        self.dollar_gain = []
        # Array for percentage gain per trade
        self.pct_gain = []
    
    def buy(self, price):
        # Buy Action
        self.buy_at = price
        self.is_holding = True
        # Buy Power with capital
        if self.capital is not None:
            self.share = self.capital // self.buy_at
            if self.max_share is not None and self.share > self.max_share:
                self.share = self.max_share
            self.capital -= np.round(self.buy_at * self.share, 2)
    
    def sell(self, price):
        # Sell Action
        self.calculate_gain(price)
        if self.capital is not None:
            self.capital += np.round(price * self.share)
            self.share = 0
        self.buy_at = 0
        self.is_holding = False
    
    def calculate_gain(self, price):
        dollar_gain = price - self.buy_at
        pct_gain = price / self.buy_at - 1
        self.dollar_gain.append(dollar_gain)
        self.pct_gain.append(pct_gain)
    
    def show_results(self):
        self.results = self.result_Series()
        print('Average gain of ${:.2f} per share after {} trades'.format(self.results['Total-Dollar-Gain'], 
                                                                self.results['Num-Trades']))
        print('and have average gain percentage of {:.2f}%'.format(self.results['Total-Percentage-Gain'] * 100))
        print('Has a {:.2f}% of good trades'.format(self.results['Percentage-of-Good-Trades'] * 100))
        if self.capital is not None:
            print('Test Ending Capital: ${:.2f} base on original capital of ${:.2f}'.format(self.capital, self.original_capital))
            print('With {:.2f}% Capital Gain'.format(self.results['Percentage-Capital-Gain'] * 100))
        self.original_capital = self.capital

    def result_Series(self):
        index = ['Num-Trades', 'Total-Dollar-Gain', 'Total-Percentage-Gain', 
                 'Percentage-of-Good-Trades','Percentage-Capital-Gain']
        num_trades = len(self.dollar_gain)
        total_dollar_gain = np.mean(self.dollar_gain)
        total_pct_gain = np.mean(self.pct_gain)
        pct_good_trades = (np.array(self.dollar_gain) > 0).sum() / num_trades
        array = [num_trades, total_dollar_gain, total_pct_gain, pct_good_trades]
        if self.capital is not None:
            capital_gain = self.capital / self.original_capital - 1
            array.append(capital_gain)
            return pd.Series(array, index=index)
        return pd.Series(array, index=index[:-1])
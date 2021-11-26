import pandas as pd

class Strategy:
    def __init__(self, fast=3, slow=6):
        self.a = fast
        self.b = slow
        self.apct = None
    
    def update_apct(self, df):
        # Calcualte Periodic High Low gap
        rolled_low = df['Low'].shift(self.a)
        pct = df['High'] / rolled_low - 1
        # Getting Average Gap base on data
        self.apct = pct.mean()
    
    def update_data(self, df):
        self.data = self.crossing_data(df)
        self.data = self.get_good_trades(self.data)
    
    def crossing_data(self, df):
        # MA Crossing or Conditional 
        fast_ma = df['Close'].rolling(self.a).mean()
        slow_ma = df['Low'].rolling(self.b).mean()
        above = fast_ma > slow_ma
        # Concatenate MA and Crossing
        data = pd.concat([fast_ma, slow_ma, above], axis=1)
        data.columns = ['fast_ma', 'slow_ma', 'above']
        # Concatenate DF with MA
        data = pd.concat([df.loc[:, ['High', 'Low', 'Close']], data], axis=1)
        return data.dropna()
    
    def get_good_trades(self, df):
        rolled_high = df['High'].shift(self.a)
        # Adjusted High is like a padding for first requirement of a good buy price
        adjusted_high = rolled_high * (1. - self.apct) 
        # Current Low Price against Adjusted High Price to get a percent different
        pricing = df['Low'] / adjusted_high - 1
        # Check if the percent different is lesser than the average gap
        # which would result in a good buy of the Low price
        df['Good-Buy'] = pricing <= self.apct
        return df.dropna()
import os, datetime
import pandas as pd
from yfQuery import datareader

class DataLoader:
    def __init__(self, symbol, years=10, dname='Database', need_update=False):
        self.symbol = symbol
        self.yrs = years
        self.directory = os.path.join(os.getcwd(), dname)
        self.filename = self.symbol + '.csv'
        # Create Database directory if doesn't exist
        if not os.path.isdir(self.directory):
            os.mkdir(self.directory)
        # Check if symbol in database or need_update
        if not os.path.exists(os.path.join(self.directory, self.filename)) or need_update:
            # Download data then load
            self.update_database()
        else:
            # Load data
            self.load_data()
    
    def get_data(self, start, end):
        assert isinstance(start, str) or isinstance(start, int), "Check start date or index"
        assert isinstance(end, str) or isinstance(end, int), "Check end date or index"
        # Get a set period of data
        if isinstance(start, str) and isinstance(end, str):
            m = self.data.index.isin(pd.date_range(start, end))
            return self.data.loc[m]
        elif isinstance(start, int) and isinstance(end, int):
            return self.data.iloc[start: end]
        else:
            print('DataType mismatch!')
        
    def load_data(self):
        # loading data from Database
        self.data = pd.read_csv(os.path.join(self.directory, self.filename), index_col=0, header=0)
        self.data.index = pd.to_datetime(self.data.index, format='%Y%m%d %H:%M:%S')
    
    def update_database(self):
        # Get today to use as ending date
        today = datetime.date.today()
        # Get start time base on lookback years 
        previous = today - datetime.timedelta(days=365*self.yrs)
        # Downloading price data
        df = datareader(self.symbol, str(previous), str(today))
        # Storing price data
        df.to_csv(os.path.join(self.directory, self.filename))
        self.data = df.dropna()
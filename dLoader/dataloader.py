from yfQuery import datareader

class DataLoader:
    '''
        Class for loading past stocks prices
        symbol: symbol can be either a single symbol or 
                a list of symbol
        start:  start date
        end:    end date
    '''
    def __init__(self, symbol, start, end):
        # Preload
        self.data = datareader(symbol, start, end)
    
    def get(self, start, end):
        # Return a period of the data
        return self.data.iloc[start: end]
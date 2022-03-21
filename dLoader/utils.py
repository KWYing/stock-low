import numpy as np
import pandas as pd

# Use for accurate regrouping of price data from type: DataFrame
def batching(df, batch_size: int):
    # Batching or resizing 
    num_batches = len(df) // batch_size
    max_length = num_batches * batch_size
    return np.array(df)[-max_length:].reshape(-1, batch_size)

def single_ordering(data):
    ol = data['Open'] / data['Low'] - 1
    cl = data['Close'] / data['Low'] - 1
    mask = ol < cl
    data['First'] = data['High']
    data['Second'] = data['Low']
    data.loc[mask, 'First'] = data.loc[mask, 'Low']
    data.loc[mask, 'Second'] = data.loc[mask, 'High']
    return data

def ordering(highs, lows):
    hmask = np.argsort(highs)[:, -1]
    lmask = np.argsort(lows)[:, 0]
    first, second = [], []
    for i, (h, l) in enumerate(zip(hmask, lmask)):
        if h < l:
            first.append(highs[i, h])
            second.append(lows[i, l])
        else:
            first.append(lows[i, l])
            second.append(highs[i, h])
    return np.array(first), np.array(second)

def regroup(df, period: int, order=False):
    if period == 1:
        if order:
            return single_ordering(df)
        return df
    # Regroup prices and volume
    opens = batching(df['Open'], period)[:, 0]
    high = batching(df['High'], period).max(1)
    low = batching(df['Low'], period).min(1)
    close = batching(df['Close'], period)[:, -1]
    volume = batching(df['Volume'], period).sum(1)
    # Regroup Timestamp
    timestamp = batching(df.index, period)[:, 0]
    # Return regrouped DataFrame
    if order:
        first, second = ordering(batching(df['High'], period), batching(df['Low'], period))
        return pd.DataFrame(np.stack([opens, high, low, close, volume, first, second], axis=1),
                        columns=['Open', 'High', 'Low', 'Close', 'Volume', 'First', 'Second'],
                        index=timestamp)
    return pd.DataFrame(np.stack([opens, high, low, close, volume], axis=1),
                        columns=['Open', 'High', 'Low', 'Close', 'Volume'],
                        index=timestamp)

import numpy as np
import pandas as pd

# Use for accurate regrouping of price data from type: DataFrame
def batching(df, batch_size: int):
    # Batching or resizing 
    num_batches = len(df) // batch_size
    max_length = num_batches * batch_size
    return np.array(df)[-max_length:].reshape(-1, batch_size)

def regroup(df, period: int):
    if period == 1:
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
    return pd.DataFrame(np.stack([opens, high, low, close, volume], axis=1),
                        columns=['Open', 'High', 'Low', 'Close', 'Volume'],
                        index=timestamp)

import numpy as np
import pandas as pd

### Psudo Minute Price Generator ###
def generate_df(price, m='min', randomize_swap=False):
    # Generate psudo price for minutes data
    # Creating array
    period = 390 # 390 minutes in a single trading day
    length = period * 4
    array = np.zeros(length)
    pad = int(length * .1)
    point_a = np.random.randint(pad, int(length * .6))
    point_b = np.random.randint(point_a + pad, length - pad)
    # Swapping High and Low
    if randomize_swap:
        # Randomize
        swap = np.random.choice([True, False])
    else:
        # Calculate to see if Low need to be swap
        open_to_low = price['Open'] / price['Low'] - 1
        close_to_low = price['Close'] / price['Low'] - 1
        swap = True if close_to_low > open_to_low else False
    if swap:
        pr = price['Open'], price['Low'], price['High'], price['Close']
    else:
        pr = price['Open'], price['High'], price['Low'], price['Close']
    array[[0, point_a, point_b, -1]] = pr
    # Filling gap
    fill_gap(array)
    # Restack
    restack = restack_array(array, p=period)
    # DataFrame
    date_index = create_datetime(price.name, period=period)
    df = to_dataframe(restack, date_index)
    return get_different_time_frame(df, m=m)

### Price Recursion ###
def get_bound(cur, high, low, p1, p2):
    # Finding bounds for getting prices
    upper = (high - cur) * p1
    lower = (low - cur) * p2
    gain = cur + np.random.uniform(0, upper)
    lost = cur + np.random.uniform(lower, 0)
    return gain, lost

def get_target_price(array, i):
    # Get next target
    target = array[i:][array[i:] > 0][0]
    # Get High and Low 
    high = array.max()
    low = array[array > 0].min()
    # Current price
    current = array[i - 1] if i != 0 else array[i]
    # Momentum
    momen = target - current
    # Randomize gain or lost percentage to create more noise
    low_ran = np.random.uniform(.1, .5)
    high_ran = np.random.uniform(.5, .9)
    if momen > 0:
        return np.random.choice(get_bound(current, high, low, high_ran, low_ran))
    return np.random.choice(get_bound(current, high, low, low_ran, high_ran))

def fill_gap(arr, i=0):
    # Using Recursion to get price when price is not 0.
    if (i + 1) == len(arr):
        return arr
    elif (arr <= 0).sum() == 0:
        return arr
    else:
        # Fill in zeros with psudo prices
        if arr[i] == 0:
            arr[i] = get_target_price(arr, i)
        fill_gap(arr, i+1)

### Stacking and DataFrame ###
def restack_array(array, p):
    # Restacking Array to Open, High, Low, Close
    narr = array.reshape(p, -1).copy()
    nclose = narr[:, -1].copy()
    nopen = narr[:, 0].copy()
    nopen[1:] = nclose[:-1]
    nhigh = narr.max(1)
    nlow = narr.min(1)
    return np.stack([nopen, 
                     np.max([nhigh, nopen], axis=0), 
                     np.min([nlow, nopen], axis=0), 
                     nclose]).T

def create_datetime(t, period=390):
    # Create minute index for date
    ts = t.replace(hour=9, minute=31)
    return pd.date_range(ts, periods=period, freq="1min")

def to_dataframe(array, index):
    # Create minute DataFrame
    return pd.DataFrame(array, index=index,
                        columns=['Open', 'High', 'Low', 'Close'])

def get_different_time_frame(df, m='min'):
    # Grouping the psudo data to perform different minutes output
    if m != 'min':
        o = df['Open'].groupby(by=pd.Grouper(freq=m)).first()
        c = df['Close'].groupby(by=pd.Grouper(freq=m)).last()
        h = df['High'].groupby(by=pd.Grouper(freq=m)).max()
        l = df['Low'].groupby(by=pd.Grouper(freq=m)).min()
        return pd.concat([o, h, l, c], axis=1)
    return df
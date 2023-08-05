# -*- coding: utf-8 -*-
from pandas import DataFrame
from ..utils import get_drift, get_offset, verify_series

def accbands(high, low, close, length=None, c=None, drift=None, mamode=None, offset=None, **kwargs):
    """Indicator: Acceleration Bands (ACCBANDS)"""
    # Validate arguments
    high = verify_series(high)
    low = verify_series(low)
    close = verify_series(close)
    length = int(length) if length and length > 0 else 20
    c = float(c) if c and c > 0 else 4
    min_periods = int(kwargs['min_periods']) if 'min_periods' in kwargs and kwargs['min_periods'] is not None else length
    mamode = mamode.lower() if mamode else 'sma'
    drift = get_drift(drift)
    offset = get_offset(offset)

    # Calculate Result
    hl_ratio  = (high - low) / (high + low)
    hl_ratio *= c
    _lower = low * (1 - hl_ratio)
    _upper = high * (1 + hl_ratio)

    if mamode is None or mamode == 'sma':
        lower = _lower.rolling(length, min_periods=min_periods).mean()
        mid   = close.rolling(length, min_periods=min_periods).mean()
        upper = _upper.rolling(length, min_periods=min_periods).mean()
    elif mamode == 'ema':
        lower = _lower.ewm(span=length, min_periods=min_periods).mean()
        mid   = close.ewm(span=length, min_periods=min_periods).mean()
        upper = _upper.ewm(span=length, min_periods=min_periods).mean()

    # Offset
    if offset != 0:
        lower = lower.shift(offset)
        mid = mid.shift(offset)
        upper = upper.shift(offset)

    # Handle fills
    if 'fillna' in kwargs:
        lower.fillna(kwargs['fillna'], inplace=True)
        mid.fillna(kwargs['fillna'], inplace=True)
        upper.fillna(kwargs['fillna'], inplace=True)
    if 'fill_method' in kwargs:
        lower.fillna(method=kwargs['fill_method'], inplace=True)
        mid.fillna(method=kwargs['fill_method'], inplace=True)
        upper.fillna(method=kwargs['fill_method'], inplace=True)

    # Name and Categorize it
    lower.name = f"ACCBL_{length}"
    mid.name = f"ACCBM_{length}"
    upper.name = f"ACCBU_{length}"
    mid.category = upper.category = lower.category = 'volatility'

    # Prepare DataFrame to return
    data = {lower.name: lower, mid.name: mid, upper.name: upper}
    accbandsdf = DataFrame(data)
    accbandsdf.name = f"ACCBANDS_{length}"
    accbandsdf.category = 'volatility'

    return accbandsdf



accbands.__doc__ = \
"""Acceleration Bands (ACCBANDS)

Acceleration Bands created by Price Headley plots upper and lower envelope
bands around a simple moving average.

Sources:
    https://www.tradingtechnologies.com/help/x-study/technical-indicator-definitions/acceleration-bands-abands/

Calculation:
    Default Inputs:
        length=10, c=4
    EMA = Exponential Moving Average
    SMA = Simple Moving Average
    HL_RATIO = c * (high - low) / (high + low)
    LOW = low * (1 - HL_RATIO)
    HIGH = high * (1 + HL_RATIO)

    if 'ema':
        LOWER = EMA(LOW, length)
        MID = EMA(close, length)
        UPPER = EMA(HIGH, length)
    else:
        LOWER = SMA(LOW, length)
        MID = SMA(close, length)
        UPPER = SMA(HIGH, length)

Args:
    high (pd.Series): Series of 'high's
    low (pd.Series): Series of 'low's
    close (pd.Series): Series of 'close's
    length (int): It's period.  Default: 10
    c (int): Multiplier.  Default: 4
    mamode (str): Two options: None or 'ema'.  Default: 'ema'
    drift (int): The difference period.   Default: 1
    offset (int): How many periods to offset the result.  Default: 0

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.DataFrame: lower, mid, upper columns.
"""
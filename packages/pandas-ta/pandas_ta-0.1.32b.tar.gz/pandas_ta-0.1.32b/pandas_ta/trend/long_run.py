# -*- coding: utf-8 -*-
from .decreasing import decreasing
from .increasing import increasing
from ..utils import get_offset, verify_series

def long_run(fast, slow, length=None, offset=None, **kwargs):
    """Indicator: Long Run"""
    # Validate Arguments
    fast = verify_series(fast)
    slow = verify_series(slow)
    length = int(length) if length and length > 0 else 2
    offset = get_offset(offset)

    # Calculate Result
    pb = increasing(fast, length) & decreasing(slow, length)  # potential bottom or bottom
    bi = increasing(fast, length) & increasing(slow, length)  # fast and slow are increasing
    long_run = pb | bi

    # Offset
    if offset != 0:
        long_run = long_run.shift(offset)

    # Handle fills
    if 'fillna' in kwargs:
        long_run.fillna(kwargs['fillna'], inplace=True)
    if 'fill_method' in kwargs:
        long_run.fillna(method=kwargs['fill_method'], inplace=True)

    # Name and Categorize it
    long_run.name = f"LR_{length}"
    long_run.category = 'trend'

    return long_run
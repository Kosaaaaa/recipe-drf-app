"""
    Calculation functions created only for testing purpose
"""
import logging
from functools import wraps

NUMERIC = int | float

_logger = logging.getLogger(__name__)


def log_call(func):
    @wraps(func)
    def with_logging(*args, **kwargs):
        _logger.info('Called: \'%s\' !!!', func.__name__)
        return func(*args, **kwargs)

    return with_logging


def add(x: NUMERIC, y: NUMERIC) -> NUMERIC:
    """Add y to x"""
    return x + y


def subtract(x: NUMERIC, y: NUMERIC) -> NUMERIC:
    """Subtract y from x"""
    return x - y


@log_call
def factorial(x: int) -> int:
    res = 1
    for i in range(2, x + 1):
        res *= i
    return res

"""
    Calculation functions created only for testing purpose
"""

NUMERIC = int | float


def add(x: NUMERIC, y: NUMERIC) -> NUMERIC:
    """Add y to x"""
    return x + y


def subtract(x: NUMERIC, y: NUMERIC) -> NUMERIC:
    """Subtract y from x"""
    return x - y


def factorial(x: int) -> int:
    res = 1
    for i in range(2, x + 1):
        res *= i
    return res

import functools
import math


def memoized(func):
    """Decorator. Caches a function's return value using functools.lru_cache."""
    return functools.lru_cache(maxsize=None)(func)


def choose(n, r, q=None):
    """Combination function (n choose r) using math.comb with optional modulo q."""
    if r < 0 or r > n or n < 0:
        return 0
    ans = math.comb(n, r)
    return ans % q if q is not None else ans


def represent_int(number):
    """Returns the int of number if number represents an integer value."""
    try:
        if int(number) == number:
            return int(number)
    except (TypeError, ValueError, AttributeError, OverflowError):
        pass
    return number


class ConstantRow:
    """An infinite row returning a constant value at any column index."""

    def __init__(self, value):
        self.value = value

    def __getitem__(self, i):
        return self.value

    def __str__(self):
        return f'[{self.value}]'

    def __repr__(self):
        return self.__str__()

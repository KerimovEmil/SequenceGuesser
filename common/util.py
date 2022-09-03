from collections.abc import Hashable, Sequence
import functools


class memoized(object):  # todo: change this to functools.lrucache
    """Decorator. Caches a function's return value each time it is called.
    If called later with the same arguments, the cached value is returned
    (not reevaluated)."""

    def __init__(self, func):
        self.func = func
        self.cache = {}

    def __call__(self, *args):
        if not isinstance(args, Hashable):
            # uncacheable. a list, for instance.
            # better to not cache than blow up.
            return self.func(*args)
        if args in self.cache:
            return self.cache[args]
        else:
            value = self.func(*args)
            self.cache[args] = value
            return value

    def __repr__(self):
        """Return the function's docstring."""
        return self.func.__doc__

    def __get__(self, obj, objtype):
        """Support instance methods."""
        return functools.partial(self.__call__, obj)


@memoized
def choose(n, r, q=None):
    if r == 0:
        return 1
    elif r == n:
        return 1
    else:
        if q is not None:
            return int(choose(n - 1, r - 1) * n / r) % q
        else:
            return int(choose(n - 1, r - 1) * n / r)


def represent_int(number):
    """Returns the int of string if string represents int"""
    if int(number) == number:
        return int(number)
    else:
        return number


class ConstantRow(Sequence):

    def __init__(self, value):
        self.value = value
        super().__init__()

    def __getitem__(self, i):
        return self.value

    def __len__(self):
        raise NotImplementedError

    def __str__(self):
        return f'[{self.value}]'

    def __repr__(self):
        return self.__str__()

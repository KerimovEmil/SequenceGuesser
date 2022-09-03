from SequenceType.Base import SequenceType
from common.util import ConstantRow
from typing import List
from functools import lru_cache
from sympy import Symbol, simplify

__author__ = 'Emil Kerimov'


class RecurrenceSequence(SequenceType):

    def __init__(self, seq):
        super().__init__(seq)

        self.dc_seq = dict()

    @lru_cache(None)
    def __bool__(self):
        """Determines if a sequence is this type"""
        self.dc_seq[-1] = ConstantRow(0)
        self.dc_seq[0] = ConstantRow(1)

        self.dc_seq[1] = self.seq

        for j in range(1, len(self.seq)):
            self.dc_seq[j + 1] = [None] * j
            # print(j, dc_sec)
            for i in range(j, len(self.dc_seq[j]) - 1):
                # # sympy example
                # term = (dc_sec[j][i] ** 2 - dc_sec[j][i - 1] * dc_sec[j][i + 1]) / dc_sec[j - 1][i]
                # dc_sec[j + 1].append(simplify(term))

                # for just numbers
                term = (self.dc_seq[j][i]**2 - self.dc_seq[j][i-1]*self.dc_seq[j][i+1])//self.dc_seq[j-1][i]
                self.dc_seq[j+1].append(term)

            ls_non_none = [x for x in self.dc_seq[j+1] if x is not None]
            is_terminated = self.check_termination(ls_non_none)
            print(self.dc_seq[j+1])
            if is_terminated:
                return True

        return False

    @staticmethod
    def check_termination(ls_seq: List[int]):
        return all(x == 0 for x in ls_seq) and (len(ls_seq) > 1)

    def get_sympy_expression(self):
        dc_seq = dict()
        dc_seq[-1] = ConstantRow(0)
        dc_seq[0] = ConstantRow(1)

        x = Symbol('x')
        dc_seq[1] = [n - p * x for n, p in zip(self.seq[1:], self.seq)]

        for j in range(1, len(self.seq)):
            dc_seq[j + 1] = [None] * j
            # print(j, dc_sec)
            for i in range(j, len(dc_seq[j]) - 1):
                # sympy example
                term = (dc_seq[j][i] ** 2 - dc_seq[j][i - 1] * dc_seq[j][i + 1]) / dc_seq[j - 1][i]
                dc_seq[j + 1].append(simplify(term))

            ls_non_none = [x for x in dc_seq[j+1] if x is not None]
            is_terminated = self.check_termination(ls_non_none)
            # print(dc_seq[j+1])
            if is_terminated:
                return dc_seq[j][-1]
        raise AssertionError('whoops')

    @staticmethod
    def remove_scaling():
        pass

    def term_number(self, index):
        """ The ith number in the sequence. """
        pass

    def sum_term(self, n):
        """ The sum of the first n terms. """
        pass

    def seq_str(self, n):
        """
        Returns a string with the equation for each term.
        n: Sympy Symbol Object
        """
        pass

    def sum_str(self):
        """Returns a string with the equation for the sum up to the nth term. """
        pass


# 0 0 0  0  0  0  0  0  0  0 0 0 0 0 0 0 0 0
# 1 1 1  1  1  1  1  1  1  1 1 1 1 1 1 1 1 1
# 1 4 9  16 25 36 49 64 81
#   7 17 31 49 71 97 127
#     8  8  8  8  8  8


dc_sec = dict()
dc_sec[-1] = ConstantRow(0)
dc_sec[0] = ConstantRow(1)


x = Symbol('x')

ls = [6, 7, 12, 14, 24, 28, 48, 56, 96]
# dc_sec[1] = [0, 1 - 0*x, 4 - 1*x, 9 - 4*x, 16-9*x, 25-16*x, 36-25*x, 49-36*x, 64-49*x, 81-64*x, 100-81*x, 121-100*x, 144-121*x]
# dc_sec[1] = [i**2 for i in range(0, 13)]
dc_sec[1] = ls
dc_sec[1] = [n - p * x for n, p in zip(dc_sec[1][1:], dc_sec[1])]
# dc_sec[1] = [i**3 - (i-1)**3 * x for i in range(1, 13)]

for j in range(1, 5):
    dc_sec[j+1] = [None] * j
    # print(j, dc_sec)
    for i in range(j, len(dc_sec[j])-1):
        # sympy example
        term = (dc_sec[j][i]**2 - dc_sec[j][i-1]*dc_sec[j][i+1])/dc_sec[j-1][i]
        dc_sec[j+1].append(simplify(term))

        # for just numbers
        # dc_sec[j+1].append((dc_sec[j][i]**2 - dc_sec[j][i-1]*dc_sec[j][i+1])//dc_sec[j-1][i])


print(dc_sec)
# the last non-zero row of this should give a polynomial recurrence relation of the original sequence

# obj = RecurrenceSequence([i**2 for i in range(0, 13)])
obj = RecurrenceSequence(ls)
print(obj.__bool__())
print(obj.get_sympy_expression())
# x^2 - 2
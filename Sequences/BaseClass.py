from SequenceType.Geometric import GeometricSequence
from SequenceType.GeneralFib import GeneralFibonacciSequence
from SequenceType.Polynomial import PolynomialSequence
from SequenceType.Harmonic import HarmonicSequence
from SequenceType.CatalanNumber import CatalanNumberSequence
from SequenceType.RecurrenceRelation import LinearRecurrenceSequence
import sympy
from common.util import represent_int

__author__ = 'Emil Kerimov'

# TODO: Add more possible classes

ALL_TYPES = [GeometricSequence, GeneralFibonacciSequence, PolynomialSequence, HarmonicSequence,
             CatalanNumberSequence, LinearRecurrenceSequence]  # todo change the order


def ordinal(n: int) -> str:
    """Returns the ordinal string for integer n, e.g. 1 -> '1st', 2 -> '2nd'."""
    if 11 <= (n % 100) <= 13:
        suffix = 'th'
    else:
        suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')
    return f"{n}{suffix}"


class Sequence:
    def __init__(self, ls):
        self.ls = list(ls)
        self.size = len(self.ls)

        if self.size <= 2:
            raise ValueError('Sequence provided must contain at least 3 elements')

        self.type_name = None
        self.type_obj = None
        self.next_number = None
        self.expression = None

    def __bool__(self):
        try:
            _ = self.get_type()
            return True
        except (NotImplementedError, ValueError, Exception):
            return False

    def __repr__(self):
        return f"Sequence({self.ls})"

    def get_type(self):
        for seq in ALL_TYPES:
            obj = seq(self)
            if obj:
                # todo generalize the idea of special sequences of some form
                if seq.__name__ == PolynomialSequence.__name__:  # only check for the figurate sequences if polynomial
                    n = sympy.Symbol('n')
                    self.expression = obj.seq_str(n)
                    polygonal_number = obj.polygonal_number(self.expression, n)
                    if polygonal_number:
                        res_str = "_".join([seq.__name__, polygonal_number])
                self.type_name = seq.__name__
                self.type_obj = obj
                self.type_obj()  # executes the call method

                if not 'res_str' in locals():
                    res_str = self.type_name

                return res_str
        raise NotImplementedError("Not enough data to determine sequence.")

    def next_value(self):
        """Returns the next numerical value in the sequence."""
        if self.type_obj is None:
            _ = self.get_type()
        term = self.type_obj.term_number(self.size + 1)
        self.next_number = represent_int(term)
        return self.next_number

    def get_next_number(self):
        val = self.next_value()
        return f"The next number in the sequence is: {val}"

    def ith_value(self, i: int):
        """Returns the ith numerical value in the sequence."""
        if i < 1:
            raise NotImplementedError("Negative place holders are not defined yet")
        if i <= self.size:
            return represent_int(self.ls[i - 1])
        if self.type_obj is None:
            _ = self.get_type()
        term = self.type_obj.term_number(i)
        return represent_int(term)

    def get_ith_number(self, i: int):
        val = self.ith_value(i)
        return f"The {ordinal(i)} number in the sequence is: {val}"

    def get_term_str(self):
        if self.type_obj is None:
            _ = self.get_type()

        t = sympy.Symbol('T(n)')
        n = sympy.Symbol('n')
        if self.expression is None:
            self.expression = self.type_obj.seq_str(n)
        string = sympy.Eq(t, self.expression.simplify())
        return sympy.latex(string)

    def get_sum_str(self):
        raise NotImplementedError

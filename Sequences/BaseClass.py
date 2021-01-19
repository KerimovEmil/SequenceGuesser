from SequenceType.Geometric import GeometricSequence
from SequenceType.GeneralFib import GeneralFibonacciSequence
from SequenceType.Polynomial import PolynomialSequence
from SequenceType.Harmonic import HarmonicSequence
from SequenceType.CatalanNumber import CatalanNumberSequence
from SequenceType.FigurateNumbers import SquareNumberSequence, TriangularNumberSequence, PentagonalNumberSequence, \
    HexagonalNumberSequence
import sympy
from common.util import represent_int

__author__ = 'Emil Kerimov'

# TODO: Add more possible classes

# Figurate Numbers are specific polynomial sequences and should be checked for prior to the general polynomial one
ALL_TYPES = [GeometricSequence, GeneralFibonacciSequence, SquareNumberSequence, TriangularNumberSequence,
             PentagonalNumberSequence, HexagonalNumberSequence, PolynomialSequence, HarmonicSequence,
             CatalanNumberSequence]


# todo MICHELLE, make a poly type list and then check the figurate ones in there
class Sequence:
    def __init__(self, ls):
        self.ls = ls
        self.size = len(self.ls)

        if self.size <= 2:
            raise Exception('Sequence provided must contain at least 3 elements')

        self.type_name = None
        self.type_obj = None
        self.next_number = None

    def __bool__(self):
        raise NotImplementedError("not yet")

    def get_type(self):
        for seq in ALL_TYPES:
            obj = seq(self)
            if obj:
                self.type_name = seq.__name__
                self.type_obj = obj
                return self.type_name
        raise NotImplementedError("Not enough data to determine sequence.")

    def get_next_number(self):
        if self.type_obj is None:
            _ = self.get_type()
        next_number = self.type_obj.term_number(self.size + 1)
        self.next_number = represent_int(next_number)

        return "The next number in the sequence is: {}".format(self.next_number)

    def get_ith_number(self, i):
        val = None
        if i < 1:
            raise NotImplementedError("Negative place holders are not defined yet")
        if i <= self.size:
            val = self.ls[i - 1]
        if self.type_obj is None:
            _ = self.get_type()
        if val is None:
            val = self.type_obj.term_number(i)

        val = represent_int(val)

        return "The {0}th number in the sequence is: {1}".format(i, val)

    def get_term_str(self):
        if self.type_obj is None:
            _ = self.get_type()

        t = sympy.Symbol('T(n)')
        n = sympy.Symbol('n')
        expression = self.type_obj.seq_str(n).simplify()
        string = sympy.Eq(t, expression)
        return sympy.latex(string)

        # return self.type_obj.seq_str()

    def get_sum_str(self):
        raise NotImplementedError
        # if self.type_obj is None:
        #     _ = self.get_type()
        # return self.type_obj.sum_str()

from SequenceType.Base import SequenceType
import math
import numpy as np


class SquareNumberSequence(SequenceType):

    def __init__(self, seq):
        super(SquareNumberSequence, self).__init__(seq)

    def __bool__(self):
        """ Checks whether sequence contains Square Numbers"""
        if self.seq.size <= 2:
            return False

        # get the root of the first term
        root_term_1 = math.sqrt(self.seq.ls[0])
        if math.floor(root_term_1 + 0.5) ** 2 != self.seq.ls[0]:
            return False  # first term is already not a perfect square

        for i in range(1, len(self.seq.ls)):
            if (root_term_1 + i) ** 2 != self.seq.ls[i]:
                return False

        return True

    def term_number(self, index):
        return (math.sqrt(self.seq.ls[-1]) + (index - self.seq.size)) ** 2

    def seq_str(self, n):
        return n ** 2


class TriangularNumberSequence(SequenceType):

    def __init__(self, seq):
        super(TriangularNumberSequence, self).__init__(seq)
        self.n_last_term = 0  # nth term in Triangular Number Sequence for the last term of the testing sequence

    def __bool__(self):
        """ Checks whether sequence contains Triangular Numbers"""
        if self.seq.size <= 2:
            return False

        # get the nth Triangular Number
        self.n_last_term = math.floor(max(np.roots([1, 1, -(2 * self.seq.ls[-1])])))

        # last term is not a triangular number
        if (self.n_last_term * (self.n_last_term + 1)) / 2 != self.seq.ls[-1]:
            return False

        for i in range(1, self.seq.size):
            if ((self.n_last_term - i) * (self.n_last_term - i + 1)) / 2 != self.seq.ls[self.seq.size - i - 1]:
                return False
        return True

    @staticmethod
    def nth_triangular_number(n):
        """ Get the nth term triangular number """
        return n * (n + 1) / 2

    def term_number(self, index):
        """ Get the ith number in the sequence """
        req_n_term = self.n_last_term + (index - self.seq.size)
        return TriangularNumberSequence.nth_triangular_number(req_n_term)

    def seq_str(self, n):
        return n * (n + 1) / 2


class PentagonalNumberSequence(SequenceType):

    def __init__(self, seq):
        super(PentagonalNumberSequence, self).__init__(seq)
        self.n_last_term = 0  # nth term in Pentagonal Number Sequence for the last term of the testing sequence

    def __bool__(self):
        """ Checks whether sequence contains Pentagonal Numbers"""

        # get the nth Pentagonal Number
        self.n_last_term = math.floor(max(np.roots([3, -1, -(2 * self.seq.ls[-1])])))

        # last term is not a Pentagonal number
        if (self.n_last_term * (3 * self.n_last_term - 1)) / 2 != self.seq.ls[-1]:
            return False

        for i in range(1, self.seq.size):
            if ((self.n_last_term - i) * (3 * (self.n_last_term - i) - 1)) / 2 != self.seq.ls[self.seq.size - i - 1]:
                return False
        return True

    @staticmethod
    def nth_pentagonal_number(n):
        """ Get the nth term pentagonal number """
        return n * (3 * n - 1) / 2

    def term_number(self, index):
        """ Get the ith number in the sequence """
        req_n_term = self.n_last_term + (index - self.seq.size)
        return PentagonalNumberSequence.nth_pentagonal_number(req_n_term)

    def seq_str(self, n):
        return n * (3 * n - 1) / 2

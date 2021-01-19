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


class HexagonalNumberSequence(SequenceType):

    def __init__(self, seq):
        super(HexagonalNumberSequence, self).__init__(seq)
        self.n_last_term = 0  # nth term in Pentagonal Number Sequence for the last term of the testing sequence

    def __bool__(self):
        """ Checks whether sequence contains Hexagonal Numbers"""

        # get the nth Hexagonal Number
        self.n_last_term = math.floor(max(np.roots([4, -2, -(2 * self.seq.ls[-1])])))

        # last term is not a Hexagonal number
        if (2 * self.n_last_term * (2 * self.n_last_term - 1)) / 2 != self.seq.ls[-1]:
            return False

        for i in range(1, self.seq.size):
            if (2 * (self.n_last_term - i) * (2 * (self.n_last_term - i) - 1)) / 2 != \
                    self.seq.ls[self.seq.size - i - 1]:
                return False
        return True

    @staticmethod
    def nth_hexagonal_number(n):
        """ Get the nth term hexagonal number """
        return 2 * n * (2 * n - 1) / 2

    def term_number(self, index):
        """ Get the ith number in the sequence """
        req_n_term = self.n_last_term + (index - self.seq.size)
        return HexagonalNumberSequence.nth_hexagonal_number(req_n_term)

    def seq_str(self, n):
        return 2 * n * (2 * n - 1) / 2


class CentralPolygonalSequence(SequenceType):

    def __init__(self, seq):
        super(CentralPolygonalSequence, self).__init__(seq)
        self.n_last_term = 0  # nth term in Central Polygonal Number Sequence for the last term of the testing sequence

    def __bool__(self):
        """ Checks whether sequence contains Central Polygonal Numbers (Lazy Caterer's Sequence)"""

        # get the nth Central Polygonal Number
        self.n_last_term = math.floor(max(np.roots([1, 1, 2 - (2 * self.seq.ls[-1])])))

        # last term is not a Central Polygonal number
        if (self.n_last_term ** 2 + self.n_last_term + 2) / 2 != self.seq.ls[-1]:
            return False

        for i in range(1, self.seq.size):
            if ((self.n_last_term - i) ** 2 + ((self.n_last_term - i) + 2)) / 2 != \
                    self.seq.ls[self.seq.size - i - 1]:
                return False
        return True

    @staticmethod
    def nth_central_polygonal_number(n):
        """ Get the nth term central polygonal number """
        return (n ** 2 + n + 2) / 2

    def term_number(self, index):
        """ Get the ith number in the sequence """
        req_n_term = self.n_last_term + (index - self.seq.size)
        return CentralPolygonalSequence.nth_central_polygonal_number(req_n_term)

    def seq_str(self, n):
        return (n ** 2 + n + 2) / 2

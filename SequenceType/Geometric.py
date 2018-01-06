from SequenceType.Base import SequenceType
from common.util import represent_int

__author__ = 'Emil Kerimov'


class GeometricSequence(SequenceType):

    def __init__(self, seq):
        super(GeometricSequence, self).__init__(seq)

        if self.seq.ls[0] == 0:
            self.ratio = None
        else:
            self.ratio = self.seq.ls[1] / self.seq.ls[0]

    def __bool__(self):
        """Determines if a sequence of numbers is a geometric sequence, returns true or false"""
        if self.seq.size <= 2:
            return False
        if self.ratio is None:
            return False
        r = self.seq.ls
        for i in range(self.seq.size - 1):
            if self.ratio != r[i + 1] / r[i]:
                return False
        return True

    def term_number(self, index):
        """ The ith number in the sequence. """
        return self.seq.ls[0] * (self.ratio ** (index - 1))

    def sum_term(self, n):
        """ The sum of the first n terms. """
        return self.seq.ls[0] * (self.ratio ** n - 1) / (self.ratio - 1)

    def seq_str(self, n):
        a = represent_int(self.seq.ls[0])
        r = represent_int(self.ratio)
        expression = a * r**n
        return expression

    def sum_str(self):
        return None

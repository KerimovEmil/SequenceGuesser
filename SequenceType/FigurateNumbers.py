from SequenceType.Base import SequenceType
import math


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
        return (math.sqrt(self.seq.ls[-1]) + (index - len(self.seq.ls))) ** 2

    def seq_str(self, n):
        return n ** 2

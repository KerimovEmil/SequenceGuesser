from SequenceType.Base import SequenceType
from SequenceType.Polynomial import PolynomialSequence
import copy


class HarmonicSequence(SequenceType):

    def __init__(self, seq):
        super(HarmonicSequence, self).__init__(seq)
        seq_copy = copy.deepcopy(seq)
        seq_copy.ls = [1 / x for x in seq.ls]

        self.reciprocal_seq = seq_copy
        self.potential_poly_seq = PolynomialSequence(self.reciprocal_seq)

    def __bool__(self):
        # if reciprocals are arithmetic sequence
        poly_bool = self.potential_poly_seq.__bool__()
        return poly_bool

    def term_number(self, index):
        return 1 / self.potential_poly_seq.term_number(index)

    def seq_str(self, n):
        return 1 / self.potential_poly_seq.seq_str(n)

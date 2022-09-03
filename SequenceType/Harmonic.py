from SequenceType.Base import SequenceType
from SequenceType.Polynomial import PolynomialSequence
import copy


class HarmonicSequence(SequenceType):

    def __init__(self, seq):
        super().__init__(seq)

    def __bool__(self):
        if any(x == 0 for x in self.seq.ls):
            return False

        reciprocal_seq = copy.deepcopy(self.seq)
        reciprocal_seq.ls = [1 / x for x in self.seq.ls]

        self.potential_poly_seq = PolynomialSequence(reciprocal_seq)

        # if reciprocals are arithmetic sequence
        poly_bool = self.potential_poly_seq.__bool__()
        return poly_bool

    def term_number(self, index):
        return 1 / self.potential_poly_seq.term_number(index)

    def seq_str(self, n):
        return 1 / self.potential_poly_seq.seq_str(n)

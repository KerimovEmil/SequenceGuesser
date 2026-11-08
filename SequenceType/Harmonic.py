from SequenceType.Base import SequenceType
from SequenceType.Polynomial import PolynomialSequence
from fractions import Fraction
import copy


class HarmonicSequence(SequenceType):

    def __init__(self, seq):
        super().__init__(seq)
        self.potential_poly_seq = None

    def __bool__(self):
        if any(x == 0 for x in self.seq.ls):
            return False

        try:
            reciprocal_seq = copy.deepcopy(self.seq)
            reciprocal_seq.ls = [
                1 / (Fraction(x).limit_denominator(10**9) if isinstance(x, float) else Fraction(x))
                for x in self.seq.ls
            ]
            reciprocal_seq.ls = [
                int(r) if r.denominator == 1 else r
                for r in reciprocal_seq.ls
            ]
        except (ValueError, TypeError, ZeroDivisionError):
            return False

        self.potential_poly_seq = PolynomialSequence(reciprocal_seq)
        poly_bool = bool(self.potential_poly_seq)
        return poly_bool

    def term_number(self, index):
        val = self.potential_poly_seq.term_number(index)
        if any(isinstance(x, float) for x in self.seq.ls):
            return float(1 / val)
        return 1 / val

    def seq_str(self, n):
        return 1 / self.potential_poly_seq.seq_str(n)

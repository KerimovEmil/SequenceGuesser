from SequenceType.Base import SequenceType
import math
from sympy import factorial


class CatalanNumberSequence(SequenceType):  # todo make this only be tested if it is a particular recurrence relation

    def __init__(self, seq):
        super(CatalanNumberSequence, self).__init__(seq)
        self.n = 0  # nth catalan number.  Number in the 0,1,2,3,etc. catalan sequence

    @staticmethod
    def nth_catalan_number(n):
        """ Get the nth term catalan number """
        if n < 0:
            return 0
        return math.comb(2 * n, n) // (n + 1)

    def __bool__(self):
        """ Check whether sequence is Catalan Numbers """
        for val in self.seq.ls:
            if not isinstance(val, int) and not (isinstance(val, float) and val.is_integer()):
                return False

        first = int(self.seq.ls[0])
        if first < 1:
            return False

        if first == 1:
            if int(self.seq.ls[1]) == 1:
                self.n = 0
            elif int(self.seq.ls[1]) == 2:
                self.n = 1
            else:
                return False
        else:
            c = 1
            k = 0
            while c < first:
                k += 1
                c = c * 2 * (2 * k - 1) // (k + 1)
            if c != first:
                return False
            self.n = k

        for i in range(1, self.seq.size):
            if int(self.seq.ls[i]) != self.nth_catalan_number(self.n + i):
                return False

        return True

    def term_number(self, index):
        """ The ith number in the sequence """
        n = self.n + index - 1
        return CatalanNumberSequence.nth_catalan_number(n)

    def seq_str(self, n):
        n_repr = self.n - 1
        expression = factorial(2 * (n + n_repr)) / (factorial(n + n_repr + 1) * factorial(n + n_repr))
        return expression

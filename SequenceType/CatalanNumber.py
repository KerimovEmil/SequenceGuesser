from SequenceType.Base import SequenceType
from scipy.special import comb
from scipy.optimize import fsolve
from sympy import factorial


class CatalanNumberSequence(SequenceType):

    def __init__(self, seq):
        super(CatalanNumberSequence, self).__init__(seq)
        self.n = 0  # nth catalan number.  Number in the 0,1,2,3,etc. catalan sequence

    def __bool__(self):
        """ Check whether sequence is Catalan Numbers """

        # solve for the catalan term position of the first number
        # arbitrarily start with initial guess of 5
        # todo think about this because it won't work with much larger numbers
        self.n = round(fsolve(lambda x: (comb(2 * x, x) * 1 / (x + 1)) - self.seq.ls[0], 5)[0])

        if self.n == 1 and self.seq.ls[1] == 1:
            self.n = 0

        for i in range(1, self.seq.size):
            if self.seq.ls[i] != comb(2 * (self.n + i), self.n + i) * 1 / (self.n + i + 1):
                return False

        return True

    @staticmethod
    def nth_catalan_number(n):
        """ Get the nth term catalan number """
        return comb(2 * n, n) * 1 / (n + 1)

    def term_number(self, index):
        """ The ith number in the sequence """
        n = self.n + index - 1

        return CatalanNumberSequence.nth_catalan_number(n)

    def seq_str(self, n):
        n_repr = self.n - 1
        expression = factorial(2 * (n + n_repr)) / (factorial(n + n_repr + 1) * factorial(n + n_repr))
        return expression

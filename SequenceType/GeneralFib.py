from SequenceType.Base import SequenceType
import sympy

__author__ = 'Emil Kerimov'


class GeneralFibonacciSequence(SequenceType):

    def __init__(self, seq):
        super(GeneralFibonacciSequence, self).__init__(seq)

        self.a = self.seq.ls[0]
        self.b = self.seq.ls[1]

    def __bool__(self):
        """Determines if a sequence of numbers is almost a fibonacci sequence, returns true or false"""
        if self.seq.size <= 2:
            return False
        r = self.seq.ls
        for i in range(self.seq.size - 2):
            if r[i] + r[i + 1] != r[i + 2]:
                return False
        return True

    @staticmethod
    def nth_fibonacci_term(n):
        # TODO: Improve efficiency of this function, and more precision
        sqrt5 = 5 ** 0.5
        phi = (1 + sqrt5) / 2
        # c_phi = 1 - phi
        # return (phi ** n - c_phi ** n) / sqrt5
        if n > 0:
            return round(phi ** n / sqrt5 )
        else:
            raise NotImplementedError('Negative Fibonacci is not implemented yet.')

    def term_number(self, index):
        """ The ith number in the sequence. """
        out = self.a * GeneralFibonacciSequence.nth_fibonacci_term(index-2)
        out += self.b * GeneralFibonacciSequence.nth_fibonacci_term(index-1)
        return out

    def seq_str(self, n):
        # f = sympy.Function('f')
        f_n2 = (((1 + sympy.sqrt(5))/2)**(n-2) + ((1 - sympy.sqrt(5))/2)**(n-2)) / sympy.sqrt(5)
        f_n1 = (((1 + sympy.sqrt(5))/2)**(n-1) + ((1 - sympy.sqrt(5))/2)**(n-1)) / sympy.sqrt(5)
        expression = self.a * f_n2 + self.b * f_n1

        return expression

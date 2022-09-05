from SequenceType.Base import SequenceType
from common.util import choose, memoized
import sympy
import math

__author__ = 'Emil Kerimov'


class PolynomialSequence(SequenceType):

    def __init__(self, seq):
        super(PolynomialSequence, self).__init__(seq)

        self.level = None

    def __bool__(self):
        d = PolynomialSequence.difference(self.seq.ls)
        self.level = 1
        while len(d) > 1:
            # loop while more than 1 difference exists
            if len(set(d)) == 1:
                return True
            else:
                d = PolynomialSequence.difference(d)
                self.level += 1
        return False

    @staticmethod
    def difference(ls):
        return [ls[i + 1] - ls[i] for i in range(len(ls) - 1)]

    def term_number(self, index):
        """ The ith number in the sequence. """
        number = 0
        for diff in range(self.level + 1):
            number += choose(index - 1, diff) * self.first(diff)
        return number

    @memoized
    def first(self, diff):
        """Returns the first number of each of the sequences"""
        # if diff == 0:
        #   r[0]
        # if diff ==1:
        #    r[1]-r[0]
        # if diff==2:
        #    (r[2]-r[1])-(r[1]-r[0])
        #     r[2] -2 r[1] + r[0]
        # if diff==3:
        #  ((r[3]-r[2])-(r[2]-r[1])) - ((r[2]-r[1])-(r[1]-r[0]))
        #    r[3] - 3r[2] + 3r[1] - r[0]
        # therefore
        # if diff=n
        # (n/0)*r[n] - (n/1)*r[n-1] +(n/2)*r[n-2] - (n/3)*r[n-3] ....+ (n/n)*r[0]
        out = 0
        for i in range(diff + 1):
            out += choose(diff, i) * self.seq.ls[diff - i] * ((-1) ** i)

        return out

    def seq_str(self, n):

        def f(d):
            """Returns (1/d!)(n-1)(n-2)...(n-d)"""
            w = 1
            for i in range(1, d + 1):
                w *= (n - i) / i
            return w

        expression = 0
        for diff in range(self.level + 1):
            expression += f(diff) * self.first(diff)
        # str(r[0]) + " + (n-1)" + str(r[1] - r[0]) + " + (1/2)(n-1)(n-2)" + str(r[2] - 2 * (r[1] - r[0]) - r[0])
        return expression

    def sum_str(self):
        return None

    def polygonal_number(self, input_expression, n):
        """
        Check whether the polynomial sequence is also a regular convex polygonal number sequence
        Checks up to 20 sides

        Args:
            input_expression: <sympy.core.add.Add> expression of the sequence
            n: <sympy.core.symbol.Symbol> symbol n, term number in the sequence

        Returns:
            <str> Polygonal Number sequence name i.e. RegularConvexPolygonal_TrigonalNumbers, or False if not one

        """
        dict_type = {3: 'TrigonalNumbers',
                     4: 'TetragonalNumbers',
                     5: 'PentagonalNumbers',
                     6: 'HexagonalNumbers',
                     7: 'HeptagonalNumbers',
                     8: 'OctagonalNumbers',
                     9: 'NonagonalNumbers',
                     10: 'DecagonalNumbers',
                     11: 'HendecagonalNumbers',
                     12: 'DodecagonalNumbers',
                     13: 'TridecagonalNumbers',
                     14: 'TetradecagonalNumbers',
                     15: 'PentadecagonalNumbers',
                     16: 'HexadecagonalNumbers',
                     17: 'HeptadecagonalNumbers',
                     18: 'OctadecagonalNumbers',
                     19: 'NonadecagonalNumbers',
                     20: 'IcosagonalNumbers'}

        # if first number is a negative number, return false
        if self.seq.ls[0] < 0:
            return False

        n = sympy.Symbol('n')

        # get number of sides
        res_V = False
        for V in range(3, 21):
            # use the first term to get the 'nth' number
            reg_conv_poly_expr = (n / 2) * ((V - 2) * n - (V - 4))
            eqn = sympy.Eq(reg_conv_poly_expr, self.seq.ls[0])

            root = math.floor(max(list(sympy.solve(eqn, n))).evalf())
            if reg_conv_poly_expr.subs(n, root) != self.seq.ls[0]:
                continue

            # root is the nth polygonal number of the first sequence term
            if sympy.simplify(input_expression.subs(n, n - (root - 1)) - reg_conv_poly_expr) == 0:
                res_V = V
                break

        res = dict_type.get(res_V, False)

        if not res:
            return False
        else:
            return '_'.join(['RegularConvexPolygonal', res])

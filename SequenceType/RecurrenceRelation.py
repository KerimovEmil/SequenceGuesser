from SequenceType.Base import SequenceType
from common.util import ConstantRow
from typing import List, Dict
from functools import lru_cache
from sympy import Symbol, simplify, solve, Matrix, gcd

__author__ = 'Emil Kerimov'


class LinearRecurrenceSequence(SequenceType):

    def __init__(self, seq):
        super().__init__(seq)

        self.dc_seq = dict()

    @lru_cache(None)
    def __bool__(self):
        """Determines if a sequence is this type"""
        self.dc_seq[-1] = ConstantRow(0)
        self.dc_seq[0] = ConstantRow(1)

        self.dc_seq[1] = self.seq.ls

        for j in range(1, self.seq.size):
            self.dc_seq[j + 1] = [None] * j
            for i in range(j, len(self.dc_seq[j]) - 1):
                # for just numbers
                term = self.get_next_item(self.dc_seq, row=j, col=i)
                self.dc_seq[j+1].append(term)

            ls_non_none = [x for x in self.dc_seq[j+1] if x is not None]
            is_terminated = self.check_termination(ls_non_none)
            if is_terminated:
                return True

        return False

    @staticmethod
    def get_next_item(dc: Dict[int, List[int]], row: int, col: int):

        # solve the formula x*d[row-1,col] + d[row-1,col]*d[row+1,col] = d[row,col]^2
        if dc[row-1][col] != 0:
            term = (dc[row][col]**2 - dc[row][col-1]*dc[row][col+1]) / dc[row-1][col]
        else:
            # if d[row-1,col] is 0 then solves the following equation:
            # x * d[row - 2, col]^2 + d[row-3,col] * d[row,col]^2
            # = d[row-1, col-1]^2 * d[row-1, col+2] + d[row-1, col+1]^2 * d[row-1, col-2]
            if dc[row-2][col] != 0:
                num = dc[row-1][col-1]**2 * dc[row-1][col+2] + dc[row-1][col+1]**2 * dc[row-1][col-2] - \
                      dc[row][col]**2 * dc[row-3][col]
                term = num / (dc[row - 2][col]**2)
            else:
                raise NotImplementedError('need to implement general square of zeros handling')

        return term

    @staticmethod
    def check_termination(ls_seq: List[int]):
        return all(x == 0 for x in ls_seq) and (len(ls_seq) > 1)

    @lru_cache(maxsize=1)
    def get_sympy_expression(self):
        dc_seq = dict()
        dc_seq[-1] = ConstantRow(0)
        dc_seq[0] = ConstantRow(1)

        x = Symbol('x')
        dc_seq[1] = [n - p * x for n, p in zip(self.seq.ls[1:], self.seq.ls)]

        for j in range(1, self.seq.size):
            dc_seq[j + 1] = [None] * j
            # print(j, dc_sec)
            for i in range(j, len(dc_seq[j]) - 1):
                # sympy example
                term = self.get_next_item(dc_seq, row=j, col=i)
                dc_seq[j + 1].append(simplify(term))

            ls_non_none = [x for x in dc_seq[j+1] if x is not None]
            is_terminated = self.check_termination(ls_non_none)
            # print(dc_seq[j+1])
            if is_terminated:
                return dc_seq[j][-1].factor(), x
        raise AssertionError('whoops')

    def __call__(self):
        super().__call__()

        if not self.__bool__():
            raise NotImplementedError

        self.sympy_generating_function, self.x = self.get_sympy_expression()
        self.coeff, self.terms = self.get_analytic_expression()
        self.sympy_analytic, self.n = self.create_sympy_analytic()

    @lru_cache(maxsize=1)
    def get_analytic_expression(self):
        roots = solve(self.sympy_generating_function, self.x)
        degree = self.sympy_generating_function.as_poly().degree()

        if degree != len(roots):
            raise NotImplementedError('will implement repeated roots later')

        # build matrix to solve for all the coefficients
        coeff_matrix = [[None for x in range(degree)] for y in range(degree)]
        # e.g. with sequence = 6,7,12,14,24,28,etc.
        # roots = sqrt(2), -sqrt(2)
        # equation: a*(sqrt(2))^n + b*(-sqrt(2))^n
        # n=0 -> a+b=6 -> (1  1) (a) = (6)
        # n=1 -> a-b=7    (1 -1) (b)   (7)
        for n in range(degree):
            coeff_matrix[n] = [simplify(root**n) for root in roots]
        coeff_matrix = Matrix(coeff_matrix)

        # create b vector: Ax=b
        b = Matrix(self.seq.ls[:degree])

        # coefficients  # todo, this matrix inverse is too slow for harder cases, might switch to numeric instead
        coeff = coeff_matrix.inv(method='GE') @ b

        # general terms, in case of repeated roots this is more complicated
        terms = roots

        return coeff, terms

    @lru_cache(maxsize=1)
    def get_underlying_recurrence_relation(self) -> str:
        """
        Replace generating function with recurrence relation.
        i.e.
        1) c*(x^2 - 2) -> f(n+2) = 2f(n)
        2) c*(x^2 - x - 1) -> f(n+2) = f(n+1) + f(n)
        """
        ls_coeff = self.sympy_generating_function.as_poly().all_coeffs()

        # divide by the gcd of all of these numbers, i.e. 5x^2 - 10x -> x^2 - 2x
        g = gcd(ls_coeff)
        ls_coeff_scaled = [x//g for x in ls_coeff]  # [1, 0, -2] -> x^2 + 0x - 2 = 0

        # translate powers of x as shifts in function (T operator)
        str_out = ''
        degree = len(ls_coeff_scaled)

        for d in range(len(ls_coeff_scaled)):
            # special coefficient handling
            c = ls_coeff_scaled[d]
            if c == 0:  # skip term is 0 coefficient
                continue
            elif abs(c) == 1:
                c_str = ''
            else:
                c_str = abs(c)

            # determine sign of term
            if len(str_out) == 0:
                sign = ''
            else:
                if ls_coeff_scaled[d] > 0:
                    sign = ' + '
                else:
                    sign = ' - '

            # special degree handling
            term = degree - d - 1
            if term == 0:
                term_str = 'x'
            else:
                term_str = f'x + {term}'

            str_out += sign + f'{c_str}f({term_str})'

        str_out += ' = 0'

        return str_out

    @lru_cache(maxsize=1)
    def create_sympy_analytic(self):
        n = Symbol('n')
        s = 0
        for i in range(len(self.coeff)):
            s += simplify(self.coeff[i] * (self.terms[i]**n))
        return simplify(s), n

    def term_number(self, index):
        """ The ith number in the sequence. """
        return simplify(self.sympy_analytic.subs(self.n, index-1))

    def sum_term(self, n):
        """ The sum of the first n terms. """
        pass

    def seq_str(self, n):
        """
        Returns a string with the equation for each term.
        n: Sympy Symbol Object
        """
        return self.sympy_analytic.subs(self.n, n)

    def sum_str(self):
        """Returns a string with the equation for the sum up to the nth term. """
        pass

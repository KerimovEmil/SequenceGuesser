"""Solve general Pell's equation x^2 - sqrt(D)*y^2 = n"""
import unittest


def is_int(n): return abs(n - int(n)) < 1e-13


class PellEquation:
    """Class to solve Pell Equation x^2 - d * y^2 = 1"""
    def __init__(self, d):
        self.d = d
        self.u = None

    # todo add continued fraction approach

    @staticmethod
    def generate_fundamental_solution(d=5):
        """
        Get the fundamental solution to x^2 - d*y^2 = 1, with the smallest positive value of y.
        Args:
            d: <int>, must be non-square/
        Returns: <tuple> (x,y) of solution x^2 - d*y^2 = 1, with the smallest positive value of y.
        """
        if is_int(d ** 0.5):
            return None
        y = 1
        while True:
            x2 = 1 + d * y * y
            if is_int(x2 ** 0.5):
                x = int(x2 ** 0.5)
                # only keep the positive values of x and y
                return x, y
            y += 1

    def solve_pell(self):
        if self.u is None:
            self.u = self.generate_fundamental_solution(d=self.d)
        return self.u

    def get_u_float(self):
        u1, u2 = self.solve_pell()
        return u1 + u2 * self.d**0.5

    def multiply_by_u_solution(self, x):
        """
        Multiply x with u, interpreting as numbers from the field sqrt(d). Where u is a fundamental solution.
        Args:
            x: <tuple> (a,b) to be interpreted as (a+b*sqrt(d))

        Returns: (x,y) such that (x + y*sqrt(5)) = x * u
        """
        a, b = x
        u1, u2 = self.u

        f = u1 * a + u2 * self.d * b
        s = u2 * a + u1 * b
        return f, s


class GeneralPell(PellEquation):
    """Class to solve Pell Equation x^2 - sqrt(D) * y^2 = n"""
    def __init__(self, d, n):
        super(GeneralPell, self).__init__(d)
        self.n = n
        self.solve_pell()

    def generate_primitive_solution(self, positive_only=False):
        """
        Get all possibly unique primitive generators of x^2 - d*y^2 = n
        Args:
            positive_only: <bool> specify if positive only solutions should be kept

        Returns: list of tuples (x,y) of the form (x + y*sqrt(d))
        """
        # need to check |y| <= sqrt(n*u/d)
        u, n, d = self.get_u_float(), self.n, self.d
        abs_y_threshold = int((abs(n)*u/d)**0.5)  # 12
        if n > 0:
            abs_y_min = 0
        else:
            abs_y_min = int((-n/d)**0.5) + 1  # x^2 > 0 => y > sqrt(-n/d)

        ls_tup = []
        for y in range(abs_y_min, abs_y_threshold + 1):
            x2 = n + d * y * y
            if is_int(x2 ** 0.5):
                x = int(x2 ** 0.5)
                if positive_only:
                    # only keep the positive values of x + y*sqrt(d)
                    ls_tup.append((x, y))
                    if -x + y*(d**0.5) > 0:
                        ls_tup.append((-x, y))
                    else:
                        ls_tup.append((x, -y))
                    # ls_tup.append((-x, -y))  # will always be negative
                else:
                    ls_tup.append((x, y))
                    ls_tup.append((-x, y))
                    ls_tup.append((x, -y))
                    ls_tup.append((-x, -y))

        # [(7, 1), (7, -1), (8, 2), (8, -2), (13, -5), (13, 5), (17, -7), (17, 7)]

        # filter out replicates
        ls_final_tup = ls_tup
        for sol in ls_tup:
            new_tup = self.multiply_by_u_solution(sol)
            if new_tup in ls_tup:
                # filter out the one with the negative sign purely for aesthetics
                if new_tup[1] < 0:
                    remove_tup = new_tup
                else:
                    remove_tup = sol
                ls_final_tup.remove(remove_tup)

        # [(7, 1), (7, -1), (8, 2), (8, -2), (13, -5), (17, -7)]
        return ls_final_tup

    @staticmethod
    def format_one_solution(tup, d):
        if tup[1] == 0:
            return '{}'.format(tup[0])
        if tup[1] == 1:
            return '({} + sqrt({}))'.format(tup[0], d)
        if tup[1] < 0:
            return '({} - {}*sqrt({}))'.format(tup[0], abs(tup[1]), d)
        return '({} + {}*sqrt({}))'.format(tup[0], tup[1], d)

    def format_full_solution(self, ls_tup):
        u_str = '{}^k'.format(self.format_one_solution(self.solve_pell(), self.d))
        return {self.format_one_solution(tup, self.d) + u_str for tup in ls_tup}

    def solve_general_pell(self, positive_only=False):
        ls_unique = self.generate_primitive_solution(positive_only=positive_only)
        return self.format_full_solution(ls_unique)


class TestPell(unittest.TestCase):
    def test_pell_equation(self):
        self.assertEqual(PellEquation(d=5).solve_pell(), (9, 4))

    def test_general_pell_equation(self):
        print(GeneralPell(d=6, n=3).solve_general_pell(positive_only=True))
        print(GeneralPell(d=6, n=-3).solve_general_pell(positive_only=True))

        self.assertEqual(len(GeneralPell(d=6, n=3).solve_general_pell(positive_only=True)), 1)
        self.assertEqual(len(GeneralPell(d=6, n=3).solve_general_pell()), 2)

        print(GeneralPell(d=19, n=36).solve_general_pell(positive_only=True))
        print(GeneralPell(d=19, n=36).solve_general_pell(positive_only=False))

    def test_no_general_pell_equation(self):
        """x^2 - 37*y^2 = 11 has no solution"""
        self.assertEqual(len(GeneralPell(d=37, n=11).solve_general_pell()), 0)

    def test_neg_general_pell_equation(self):
        """x^2 - 5*y^2 = -1"""
        self.assertEqual(len(GeneralPell(d=5, n=-1).solve_general_pell(positive_only=True)), 1)
        self.assertEqual(len(GeneralPell(d=5, n=-1).solve_general_pell(positive_only=False)), 3)

    def test_all_pell_equation(self):
        for d in range(2, 10):
            if is_int(d ** 0.5):
                continue
            with self.subTest('D = {}'.format(d)):
                x, y = PellEquation(d=d).solve_pell()
                # print(f'd={d}, x={x}, y={y}')
                self.assertEqual(pow(x, 2) - d * pow(y, 2), 1)

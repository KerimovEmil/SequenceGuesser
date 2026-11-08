"""Solve general Pell's equation x^2 - D*y^2 = n"""
from functools import total_ordering
import math


def is_int(n):
    return abs(n - int(n)) < 1e-13


@total_ordering
class FieldExtensionD:
    """Numbers of the form a + b*sqrt(D) for a,b integers"""

    def __init__(self, x: int, y: int, d: int):
        self.x = int(x)
        self.y = int(y)
        self.d = int(d)
        self.u_float = float(x + y * (d ** 0.5))

    def conjugate(self):
        return FieldExtensionD(x=self.x, y=-self.y, d=self.d)

    def norm(self):
        return self * self.conjugate()

    def __mul__(self, other):
        assert self.d == other.d
        f = self.x * other.x + self.y * self.d * other.y
        s = self.y * other.x + self.x * other.y
        return FieldExtensionD(x=f, y=s, d=self.d)

    def __pow__(self, power: int):
        if power < 0:
            raise NotImplementedError('Negative powers are not implemented.')
        if power == 0:
            return FieldExtensionD(x=1, y=0, d=self.d)
        result = FieldExtensionD(x=1, y=0, d=self.d)
        base = self
        p = power
        while p > 0:
            if p % 2 == 1:
                result *= base
            base *= base
            p //= 2
        return result

    def get_solutions(self):
        result = self
        while True:
            yield result
            result *= self

    def __str__(self):
        if self.y == 0:
            return f'{self.x}'
        if abs(self.y) == 1:
            if self.y > 0:
                return f'{self.x} + sqrt({self.d})'
            else:
                return f'{self.x} - sqrt({self.d})'
        if self.y < 0:
            return f'{self.x} - {abs(self.y)}*sqrt({self.d})'
        return f'{self.x} + {self.y}*sqrt({self.d})'

    def __repr__(self):
        return str(self)

    def print_generator(self):
        soln = str(self)
        return f"({soln})^k"

    def __eq__(self, other):
        if isinstance(other, FieldExtensionD):
            return (self.x == other.x) and (self.y == other.y) and (self.d == other.d)
        elif isinstance(other, (int, float)):
            return (self.x == other) and (self.y == 0)
        return False

    def __hash__(self):
        return hash((self.x, self.y, self.d))

    def __lt__(self, other):
        """Returns True if self < other """
        if abs(self.x) < abs(other.x):
            return True
        elif abs(self.x) > abs(other.x):
            return False
        else:
            if self.x > other.x:  # Assume positive x is smaller
                return True
            if abs(self.y) < abs(other.y):
                return True
            else:
                return self.y > other.y

    @staticmethod
    def remove_duplicates(fundamental_solution, pell_solutions):
        """Filter out duplicate solutions which are a multiple of each other"""
        unique_solutions = pell_solutions.copy()
        removed_solutions = set()
        for sol in pell_solutions:
            if sol in removed_solutions:
                continue
            multiple = sol * fundamental_solution
            if multiple in pell_solutions:
                if sol < multiple:
                    unique_solutions.discard(sol)
                    removed_solutions.add(sol)
                else:
                    unique_solutions.discard(multiple)
                    removed_solutions.add(multiple)
        return unique_solutions


class PellEquation:
    """Class to solve Pell Equation x^2 - d*y^2 = 1"""

    def __init__(self, d: int):
        self.d = d
        self.solution = None

    @staticmethod
    def generate_fundamental_solution(d: int = 5):
        """
        Get the fundamental solution to x^2 - d*y^2 = 1, with the smallest positive value of y.
        Uses continued fraction expansion of sqrt(d).
        Args:
            d: <int>, must be non-square
        Returns: FieldExtensionD of solution x^2 - d*y^2 = 1, with smallest positive y.
        """
        r = math.isqrt(d)
        if r * r == d:
            return None
        m = 0
        den = 1
        a = r
        p_prev, p_curr = 1, a
        q_prev, q_curr = 0, 1
        while p_curr * p_curr - d * q_curr * q_curr != 1:
            m = den * a - m
            den = (d - m * m) // den
            a = (r + m) // den
            p_prev, p_curr = p_curr, a * p_curr + p_prev
            q_prev, q_curr = q_curr, a * q_curr + q_prev
        return FieldExtensionD(x=p_curr, y=q_curr, d=d)

    def solve(self):
        if not self.solution:
            self.solution = self.generate_fundamental_solution(d=self.d)
        return self.solution


class GeneralPell(PellEquation):
    """Class to solve Pell Equation x^2 - d*y^2 = n"""

    def __init__(self, d, n):
        super().__init__(d)
        self.n = n
        self.base_solution = super().solve()  # FieldExtensionD

    def solve(self, positive_only=False):
        """
        Get all possibly unique primitive generators of x^2 - d*y^2 = n
        Args:
            positive_only: <bool> specify if positive only solutions should be kept
        Returns: set of FieldExtensionD values of the form (x + y*sqrt(d))
        """
        if self.base_solution is None:
            return set()

        u = self.base_solution.u_float
        n, d = self.n, self.d

        abs_y_threshold = int((abs(n) * u / d) ** 0.5)
        if n > 0:
            abs_y_min = 0
        else:
            abs_y_min = int((-n / d) ** 0.5) + 1

        ls_tup = set()
        for y in range(abs_y_min, abs_y_threshold + 1):
            x2 = n + d * y * y
            if x2 < 0:
                continue
            x = math.isqrt(x2)
            if x * x == x2:
                candidate_solution = FieldExtensionD(x, y, d)
                if candidate_solution.norm() == n:
                    if positive_only:
                        ls_tup.add(FieldExtensionD(x, y, d))
                        neg_x = FieldExtensionD(-x, y, d)
                        if neg_x.u_float > 0:
                            ls_tup.add(FieldExtensionD(-x, y, d))
                        else:
                            ls_tup.add(FieldExtensionD(x, -y, d))
                    else:
                        ls_tup.add(FieldExtensionD(x, y, d))
                        ls_tup.add(FieldExtensionD(-x, y, d))
                        ls_tup.add(FieldExtensionD(x, -y, d))
                        ls_tup.add(FieldExtensionD(-x, -y, d))

        return FieldExtensionD.remove_duplicates(self.base_solution, ls_tup)

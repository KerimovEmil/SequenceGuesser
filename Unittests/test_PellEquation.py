import unittest
import math
from pell_equation.general_pell import PellEquation, GeneralPell, FieldExtensionD


class TestPell(unittest.TestCase):
    def test_pell_equation(self):
        sol = PellEquation(d=5).solve()
        self.assertEqual((sol.x, sol.y), (9, 4))

    def test_pell_d61_large(self):
        # D=61 has fundamental solution (1766319049, 226153980)
        sol = PellEquation(d=61).solve()
        self.assertEqual((sol.x, sol.y), (1766319049, 226153980))
        self.assertEqual(pow(sol.x, 2) - 61 * pow(sol.y, 2), 1)

    def test_general_pell_equation(self):
        sol_pos = GeneralPell(d=6, n=3).solve(positive_only=True)
        self.assertEqual(len(sol_pos), 1)

        sol_all = GeneralPell(d=6, n=3).solve()
        self.assertEqual(len(sol_all), 2)

        sol_19_pos = GeneralPell(d=19, n=36).solve(positive_only=True)
        sol_19_all = GeneralPell(d=19, n=36).solve(positive_only=False)
        self.assertTrue(len(sol_19_pos) > 0)
        self.assertTrue(len(sol_19_all) >= len(sol_19_pos))

    def test_no_general_pell_equation(self):
        """x^2 - 37*y^2 = 11 has no solution"""
        self.assertEqual(len(GeneralPell(d=37, n=11).solve()), 0)

    def test_all_pell_equation(self):
        for d in range(2, 20):
            r = math.isqrt(d)
            if r * r == d:
                continue
            with self.subTest(f'D = {d}'):
                sol = PellEquation(d=d).solve()
                self.assertIsNotNone(sol)
                self.assertEqual(pow(sol.x, 2) - d * pow(sol.y, 2), 1)

    def test_field_extension_ops(self):
        a = FieldExtensionD(3, 2, 2)
        b = a ** 3
        # (3 + 2*sqrt(2))^3 = 27 + 3*9*2*sqrt(2) + 3*3*8 + 16*sqrt(2) = 99 + 70*sqrt(2)
        self.assertEqual((b.x, b.y), (99, 70))
        self.assertEqual(a.norm(), 1)  # 9 - 8 = 1
        self.assertEqual(b.norm(), 1)  # 99^2 - 2*70^2 = 9801 - 9800 = 1


if __name__ == '__main__':
    unittest.main()

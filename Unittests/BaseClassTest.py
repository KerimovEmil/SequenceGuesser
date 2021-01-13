from Sequences.BaseClass import Sequence
import unittest


class SequenceGuesser(unittest.TestCase):
    def test_geometric(self):
        user_input = [1, 2, 4, 8, 16, 32]
        o_seq = Sequence(user_input)

        self.assertEqual(o_seq.get_type(), 'GeometricSequence')

        out_next = o_seq.get_next_number()
        self.assertRegex(out_next, '64')

        ith_number = o_seq.get_ith_number(8)
        self.assertRegex(ith_number, '128')

    def test_harmonic_progression(self):
        user_input = [1 / 16, 1 / 13, 1 / 10, 1 / 7]
        o_seq = Sequence(user_input)

        self.assertEqual(o_seq.get_type(), 'HarmonicSequence')

        out_next = o_seq.get_next_number()
        self.assertRegex(out_next, '0.25')

        ith_number = o_seq.get_ith_number(8)
        self.assertRegex(ith_number, '-0.2')

    def test_catalan(self):
        user_input = [5, 14, 42, 132, 429, 1430]
        o_seq = Sequence(user_input)

        self.assertEqual(o_seq.get_type(), 'CatalanNumberSequence')

        out_next = o_seq.get_next_number()
        self.assertRegex(out_next, '16796') 

        ith_number = o_seq.get_ith_number(12)  # index 12
        self.assertRegex(ith_number, '9694845')

    def test_general_fib(self):
        user_input = [1, 2, 3, 5, 8, 13]
        o_seq = Sequence(user_input)

        self.assertEqual(o_seq.get_type(), 'GeneralFibonacciSequence')

        out_next = o_seq.get_next_number()
        self.assertRegex(out_next, '21')

        ith_number = o_seq.get_ith_number(8)
        self.assertRegex(ith_number, '34')

    def test_level_difference(self):
        def f(x):
            return x ** 3 + 2 * x + 2

        user_input = [f(i) for i in range(1, 10)]

        o_seq = Sequence(user_input)

        self.assertEqual(o_seq.get_type(), 'PolynomialSequence')

        out_next = o_seq.get_next_number()
        self.assertRegex(out_next, str(f(10)))

        ith_number = o_seq.get_ith_number(15)
        self.assertRegex(ith_number, str(f(15)))

    def test_constant(self):
        user_input = [6, 6, 6, 6]

        o_seq = Sequence(user_input)

        out_next = o_seq.get_next_number()
        self.assertRegex(out_next, '6')

        ith_number = o_seq.get_ith_number(15)
        self.assertRegex(ith_number, '6')

    def test_zeros(self):
        user_input = [0, 0, 0, 0]

        o_seq = Sequence(user_input)

        out_next = o_seq.get_next_number()
        self.assertRegex(out_next, '0')

        ith_number = o_seq.get_ith_number(15)
        self.assertRegex(ith_number, '0')

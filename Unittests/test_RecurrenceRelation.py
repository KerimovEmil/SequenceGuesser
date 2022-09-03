import unittest
from SequenceType.RecurrenceRelation import RecurrenceSequence


class RecurrenceRelationTest(unittest.TestCase):
    def test_every_other_term_double(self):
        ls = [6, 7, 12, 14, 24, 28, 48, 56, 96]

        class MiniSeq:
            def __init__(self, ls):
                self.ls = ls
                self.size = len(self.ls)

        obj = RecurrenceSequence(MiniSeq(ls))
        self.assertTrue(obj.__bool__())
        obj()
        # print(obj.sympy_analytic)
        for i in range(len(ls)):
            with self.subTest(msg=f'Testing {i}th number'):
                self.assertEqual(ls[i], obj.term_number(i + 1))


if __name__ == '__main__':
    unittest.main()

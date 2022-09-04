import unittest
from SequenceType.RecurrenceRelation import LinearRecurrenceSequence


class RecurrenceRelationTest(unittest.TestCase):
    def test_every_other_term_double(self):
        ls = [6, 7, 12, 14, 24, 28, 48, 56, 96]

        class MiniSeq:
            def __init__(self, ls):
                self.ls = ls
                self.size = len(self.ls)

        obj = LinearRecurrenceSequence(MiniSeq(ls))
        self.assertTrue(obj.__bool__())
        obj()
        for i in range(len(ls)):
            with self.subTest(msg=f'Testing {i}th number'):
                self.assertEqual(ls[i], obj.term_number(i + 1))

        with self.subTest(msg=f'Testing recurrence str'):
            self.assertEqual('f(x + 2) - 2f(x) = 0', obj.get_underlying_recurrence_relation())


if __name__ == '__main__':
    unittest.main()

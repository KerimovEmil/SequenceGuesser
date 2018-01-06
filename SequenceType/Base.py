__author__ = 'Emil Kerimov'


class SequenceType:

    def __init__(self, seq):
        self.seq = seq

    def __bool__(self):
        """Determines if a sequence is this type"""
        raise NotImplementedError

    def term_number(self, index):
        """ The ith number in the sequence. """
        raise NotImplementedError

    def sum_term(self, n):
        """ The sum of the first n terms. """
        raise NotImplementedError

    def seq_str(self, n):
        """
        Returns a string with the equation for each term.
        n: Sympy Symbol Object
        """
        raise NotImplementedError

    def sum_str(self):
        """Returns a string with the equation for the sum up to the nth term. """
        raise NotImplementedError

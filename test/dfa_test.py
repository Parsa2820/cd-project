import unittest
from scanner import dfa


class DFATest(unittest.TestCase):
    def test_run(self):
        pass


class TransitionTest(unittest.TestCase):
    def test_match(self):
        transition = dfa.Transition('0', '\d', '1')
        self.assertTrue(transition.match('0', '4'))


if __name__ == '__main__':
    unittest.main()

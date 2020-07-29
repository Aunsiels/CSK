import unittest

from quasimodo.data_structures.subject import Subject
from quasimodo.patterns.pattern_google import PatternGoogle


class TestGooglePatterns(unittest.TestCase):

    def test_get_str(self):
        pattern = PatternGoogle("how are <SUBJS>")
        self.assertEqual(pattern.to_str_subject(Subject("perl oyster")),
                         "how are perl oysters")


if __name__ == '__main__':
    unittest.main()

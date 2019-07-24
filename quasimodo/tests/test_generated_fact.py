import unittest

from quasimodo.generated_fact import GeneratedFact


class TestGeneratedFact(unittest.TestCase):

    def test_fact_transformation(self):
        gf = GeneratedFact("elephant", "eat", "zebra", "", False, 1.0, "elephants do not eat zebras")
        fact = gf.get_fact()
        self.assertEqual(fact.get_subject(), "elephant")
        self.assertEqual(fact.get_predicate(), "eat")
        self.assertEqual(fact.get_object(), "zebra")
        self.assertEqual(fact.is_negative(), False)
        gf = GeneratedFact("elephant", "eat", "zebra", "", True, 1.0, "elephants do not eat zebras")
        fact = gf.get_fact()
        self.assertEqual(fact.is_negative(), True)


if __name__ == '__main__':
    unittest.main()

import unittest

from quasimodo.data_structures.generated_fact import GeneratedFact
from quasimodo.data_structures.multiple_source_occurrence import MultipleSourceOccurrence


class TestGeneratedFact(unittest.TestCase):

    def test_fact_transformation(self):
        gf = GeneratedFact("elephant", "eat", "zebra", "", False, 1.0,
                           MultipleSourceOccurrence.from_raw("elephants do not eat zebras", None, 1))
        fact = gf.get_fact()
        self.assertEqual(fact.get_subject(), "elephant")
        self.assertEqual(fact.get_predicate(), "eat")
        self.assertEqual(fact.get_object(), "zebra")
        self.assertEqual(fact.is_negative(), False)
        gf = GeneratedFact("elephant", "eat", "zebra", "", True, 1.0,
                           MultipleSourceOccurrence.from_raw("elephants do not eat zebras", None, 1))
        fact = gf.get_fact()
        self.assertEqual(fact.is_negative(), True)


if __name__ == '__main__':
    unittest.main()

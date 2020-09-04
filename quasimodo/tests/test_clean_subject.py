import unittest

from quasimodo.assertion_normalization.clean_subject import CleanSubject
from quasimodo.data_structures.generated_fact import GeneratedFact
from quasimodo.data_structures.inputs import Inputs
from quasimodo.data_structures.multiple_source_occurrence import \
    MultipleSourceOccurrence


class TestCleanSubject(unittest.TestCase):

    def setUp(self) -> None:
        self.cleaning_predicate = CleanSubject(None)
        self.empty_input = Inputs()

    def test_potato(self):
        generated_fact = GeneratedFact("a potato", "be", "baked", "",
                                       False,
                                       0.0,
                                       MultipleSourceOccurrence())
        inputs = self.empty_input.add_generated_facts([generated_fact])
        inputs = self.cleaning_predicate.process(inputs)
        generated_facts = inputs.get_generated_facts()
        self.assertEqual(1, len(generated_facts))
        self.assertEqual("potato", generated_facts[0].get_subject())

    def test_nothing(self):
        generated_fact = GeneratedFact("potato", "be", "baked", "",
                                       False,
                                       0.0,
                                       MultipleSourceOccurrence())
        inputs = self.empty_input.add_generated_facts([generated_fact])
        inputs = self.cleaning_predicate.process(inputs)
        generated_facts = inputs.get_generated_facts()
        self.assertEqual(1, len(generated_facts))
        self.assertEqual("potato", generated_facts[0].get_subject())


if __name__ == '__main__':
    unittest.main()

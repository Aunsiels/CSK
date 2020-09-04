import unittest

from quasimodo.assertion_normalization.filter_language_questions import \
    FilterLanguageQuestions
from quasimodo.data_structures.generated_fact import GeneratedFact
from quasimodo.data_structures.inputs import Inputs
from quasimodo.data_structures.multiple_source_occurrence import \
    MultipleSourceOccurrence


class TestFilterLanguages(unittest.TestCase):

    def setUp(self) -> None:
        self.cleaning_predicate = FilterLanguageQuestions(None)
        self.empty_input = Inputs()

    def test_french(self):
        generated_fact = GeneratedFact("potato", "be in", "french", "",
                                       False,
                                       0.0,
                                       MultipleSourceOccurrence())
        inputs = self.empty_input.add_generated_facts([generated_fact])
        inputs = self.cleaning_predicate.process(inputs)
        generated_facts = inputs.get_generated_facts()
        self.assertEqual(0, len(generated_facts))

    def test_no_change(self):
        generated_fact = GeneratedFact("potato", "be in", "burger", "",
                                       False,
                                       0.0,
                                       MultipleSourceOccurrence())
        inputs = self.empty_input.add_generated_facts([generated_fact])
        inputs = self.cleaning_predicate.process(inputs)
        generated_facts = inputs.get_generated_facts()
        self.assertEqual(1, len(generated_facts))


if __name__ == '__main__':
    unittest.main()

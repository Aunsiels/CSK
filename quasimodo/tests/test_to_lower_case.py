import unittest

from quasimodo.data_structures.inputs import Inputs
from quasimodo.data_structures.generated_fact import GeneratedFact
from quasimodo.data_structures.multiple_scores import MultipleScore
from quasimodo.data_structures.multiple_source_occurrence import MultipleSourceOccurrence
from quasimodo.data_structures.subject import Subject
from quasimodo.assertion_normalization.to_lower_case_submodule import ToLowerCaseSubmodule


class TestToSingular(unittest.TestCase):

    def setUp(self) -> None:
        self.to_lower_case = ToLowerCaseSubmodule(None)
        self.empty_input = Inputs()

    def test_subject(self):
        generated_fact = GeneratedFact("Lions", "is a", "cat", "", False, MultipleScore(), MultipleSourceOccurrence())
        inputs = self.empty_input.add_generated_facts([generated_fact]).add_subjects({Subject("lion")})
        inputs = self.to_lower_case.process(inputs)
        generated_facts = inputs.get_generated_facts()
        self.assertEqual(1, len(generated_facts))
        self.assertEqual("lions", generated_facts[0].get_subject().get())

    def test_predicate(self):
        generated_fact = GeneratedFact("lions", "is A", "cat", "", False, MultipleScore(), MultipleSourceOccurrence())
        inputs = self.empty_input.add_generated_facts([generated_fact, generated_fact]).add_subjects({Subject("lion")})
        inputs = self.to_lower_case.process(inputs)
        generated_facts = inputs.get_generated_facts()
        self.assertEqual(2, len(generated_facts))
        self.assertEqual("is a", generated_facts[0].get_predicate().get())

    def test_object(self):
        generated_fact = GeneratedFact("lion", "is a", "cAt", "", False, MultipleScore(), MultipleSourceOccurrence())
        inputs = self.empty_input.add_generated_facts([generated_fact]).add_subjects({Subject("lion")})
        inputs = self.to_lower_case.process(inputs)
        generated_facts = inputs.get_generated_facts()
        self.assertEqual(1, len(generated_facts))
        self.assertEqual("cat", generated_facts[0].get_object().get())

    def test_do_nothing(self):
        generated_fact = GeneratedFact("crisis", "is a", "cat", "", False, MultipleScore(), MultipleSourceOccurrence())
        inputs = self.empty_input.add_generated_facts([generated_fact]).add_subjects({Subject("lion")})
        inputs = self.to_lower_case.process(inputs)
        generated_facts = inputs.get_generated_facts()
        self.assertEqual(1, len(generated_facts))
        self.assertEqual("crisis", generated_facts[0].get_subject().get())


if __name__ == '__main__':
    unittest.main()

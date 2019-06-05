import unittest

from quasimodo import Inputs
from quasimodo.generated_fact import GeneratedFact
from quasimodo.multiple_scores import MultipleScore
from quasimodo.subject import Subject
from quasimodo.to_singular_subject_submodule import ToSingularSubjectSubmodule


class TestToSingular(unittest.TestCase):

    def setUp(self) -> None:
        self.to_singular = ToSingularSubjectSubmodule(None)
        self.empty_input = Inputs()

    def test_turn_singular(self):
        generated_fact = GeneratedFact("lions", "is a", "cat", "", False, MultipleScore(), "")
        inputs = self.empty_input.add_generated_facts([generated_fact]).add_subjects({Subject("lion")})
        inputs = self.to_singular.process(inputs)
        generated_facts = inputs.get_generated_facts()
        self.assertEqual(1, len(generated_facts))
        self.assertEqual("lion", generated_facts[0].get_subject().get())

    def test_turn_singular_duplicate(self):
        generated_fact = GeneratedFact("lions", "is a", "cat", "", False, MultipleScore(), "")
        inputs = self.empty_input.add_generated_facts([generated_fact, generated_fact]).add_subjects({Subject("lion")})
        inputs = self.to_singular.process(inputs)
        generated_facts = inputs.get_generated_facts()
        self.assertEqual(2, len(generated_facts))
        self.assertEqual("lion", generated_facts[0].get_subject().get())

    def test_do_nothing(self):
        generated_fact = GeneratedFact("lion", "is a", "cat", "", False, MultipleScore(), "")
        inputs = self.empty_input.add_generated_facts([generated_fact]).add_subjects({Subject("lion")})
        inputs = self.to_singular.process(inputs)
        generated_facts = inputs.get_generated_facts()
        self.assertEqual(1, len(generated_facts))
        self.assertEqual("lion", generated_facts[0].get_subject().get())

    def test_crisis(self):
        generated_fact = GeneratedFact("crisis", "is a", "cat", "", False, MultipleScore(), "")
        inputs = self.empty_input.add_generated_facts([generated_fact]).add_subjects({Subject("lion")})
        inputs = self.to_singular.process(inputs)
        generated_facts = inputs.get_generated_facts()
        self.assertEqual(1, len(generated_facts))
        self.assertEqual("crisis", generated_facts[0].get_subject().get())

    def test_texas(self):
        generated_fact = GeneratedFact("texas", "is a", "cat", "", False, MultipleScore(), "")
        inputs = self.empty_input.add_generated_facts([generated_fact]).add_subjects({Subject("lion")})
        inputs = self.to_singular.process(inputs)
        generated_facts = inputs.get_generated_facts()
        self.assertEqual(1, len(generated_facts))
        self.assertEqual("texas", generated_facts[0].get_subject().get())


if __name__ == '__main__':
    unittest.main()
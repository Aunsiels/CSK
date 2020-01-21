import unittest

from quasimodo.assertion_normalization.can_transformation_submodule import CanTransformationSubmodule
from quasimodo.data_structures.generated_fact import GeneratedFact
from quasimodo.data_structures.inputs import Inputs
from quasimodo.data_structures.multiple_source_occurrence import MultipleSourceOccurrence
from quasimodo.patterns.pattern_google import PatternGoogle


class TestCanTransformation(unittest.TestCase):

    def setUp(self) -> None:
        self.can_transformation = CanTransformationSubmodule(None)
        self.empty_input = Inputs()

    def test_can_duplicate(self):
        generated_fact = GeneratedFact("test", "can", "can nothing", "", False, 0.0, MultipleSourceOccurrence())
        inputs = self.empty_input.add_generated_facts([generated_fact])
        inputs = self.can_transformation.process(inputs)
        generated_facts = inputs.get_generated_facts()
        self.assertEqual(1, len(generated_facts))
        self.assertEqual("can", generated_facts[0].get_predicate().get())
        self.assertEqual("nothing", generated_facts[0].get_object().get())

    def test_can_be_duplicate(self):
        generated_fact = GeneratedFact("test", "can", "can be nothing", "", False, 0.0, MultipleSourceOccurrence())
        inputs = self.empty_input.add_generated_facts([generated_fact])
        inputs = self.can_transformation.process(inputs)
        generated_facts = inputs.get_generated_facts()
        self.assertEqual(1, len(generated_facts))
        self.assertEqual("can be", generated_facts[0].get_predicate().get())
        self.assertEqual("nothing", generated_facts[0].get_object().get())

    def test_be_can_duplicate(self):
        generated_fact = GeneratedFact("test", "be", "can nothing", "", False, 0.0, MultipleSourceOccurrence())
        inputs = self.empty_input.add_generated_facts([generated_fact])
        inputs = self.can_transformation.process(inputs)
        generated_facts = inputs.get_generated_facts()
        self.assertEqual(1, len(generated_facts))
        self.assertEqual("be", generated_facts[0].get_predicate().get())
        self.assertEqual("nothing", generated_facts[0].get_object().get())

    def test_be_can_duplicate_pattern(self):
        generated_fact = GeneratedFact("test", "be", "can nothing", "", False, 0.0, MultipleSourceOccurrence(), PatternGoogle("why can <SUBJ>"))
        inputs = self.empty_input.add_generated_facts([generated_fact])
        inputs = self.can_transformation.process(inputs)
        generated_facts = inputs.get_generated_facts()
        self.assertEqual(1, len(generated_facts))
        self.assertEqual("can be", generated_facts[0].get_predicate().get())
        self.assertEqual("nothing", generated_facts[0].get_object().get())


if __name__ == '__main__':
    unittest.main()

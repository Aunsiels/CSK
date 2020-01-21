import unittest

from quasimodo.data_structures.generated_fact import GeneratedFact
from quasimodo.data_structures.inputs import Inputs
from quasimodo.data_structures.multiple_source_occurrence import MultipleSourceOccurrence
from quasimodo.assertion_normalization.present_continuous_submodule import PresentContinuousSubmodule


class TestPresentContinuous(unittest.TestCase):

    def setUp(self) -> None:
        self.present_continuous = PresentContinuousSubmodule(None)
        self.empty_input = Inputs()

    def test_nothing(self):
        generated_fact = GeneratedFact("test", "adapt", "nothing", "", False, 0.0, MultipleSourceOccurrence())
        inputs = self.empty_input.add_generated_facts([generated_fact])
        inputs = self.present_continuous.process(inputs)
        generated_facts = inputs.get_generated_facts()
        self.assertEqual(1, len(generated_facts))
        self.assertEqual("adapt", generated_facts[0].get_predicate().get())

    def test_be_ing(self):
        generated_fact = GeneratedFact("test", "is adapting", "nothing", MultipleSourceOccurrence(), False, 0.0, "")
        inputs = self.empty_input.add_generated_facts([generated_fact])
        inputs = self.present_continuous.process(inputs)
        generated_facts = inputs.get_generated_facts()
        self.assertEqual(1, len(generated_facts))
        self.assertEqual("adapt", generated_facts[0].get_predicate().get())

    def test_ing(self):
        generated_fact = GeneratedFact("test", "adapting", "nothing", "", False, 0.0, MultipleSourceOccurrence())
        inputs = self.empty_input.add_generated_facts([generated_fact])
        inputs = self.present_continuous.process(inputs)
        generated_facts = inputs.get_generated_facts()
        self.assertEqual(0, len(generated_facts))


if __name__ == '__main__':
    unittest.main()
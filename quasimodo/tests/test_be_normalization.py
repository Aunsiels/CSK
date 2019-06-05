import unittest

from quasimodo import Inputs
from quasimodo.be_normalization_submodule import BeNormalizationSubmodule
from quasimodo.generated_fact import GeneratedFact


class TestBeNormalization(unittest.TestCase):

    def setUp(self) -> None:
        self.be_normalization = BeNormalizationSubmodule(None)
        self.empty_input = Inputs()

    def test_is_alone(self):
        generated_fact = GeneratedFact("test", "is", "nothing", "", False, 0.0, "")
        inputs = self.empty_input.add_generated_facts([generated_fact])
        inputs = self.be_normalization.process(inputs)
        generated_facts = inputs.get_generated_facts()
        self.assertEqual(1, len(generated_facts))
        self.assertEqual("be", generated_facts[0].get_predicate().get())

    def test_are_alone(self):
        generated_fact = GeneratedFact("test", "are", "nothing", "", False, 0.0, "")
        inputs = self.empty_input.add_generated_facts([generated_fact])
        inputs = self.be_normalization.process(inputs)
        generated_facts = inputs.get_generated_facts()
        self.assertEqual(1, len(generated_facts))
        self.assertEqual("be", generated_facts[0].get_predicate().get())

    def test_were_alone(self):
        generated_fact = GeneratedFact("test", "were", "nothing", "", False, 0.0, "")
        inputs = self.empty_input.add_generated_facts([generated_fact])
        inputs = self.be_normalization.process(inputs)
        generated_facts = inputs.get_generated_facts()
        self.assertEqual(1, len(generated_facts))
        self.assertEqual("was", generated_facts[0].get_predicate().get())

    def test_is_not_alone(self):
        generated_fact = GeneratedFact("test", "is adapted", "nothing", "", False, 0.0, "")
        inputs = self.empty_input.add_generated_facts([generated_fact])
        inputs = self.be_normalization.process(inputs)
        generated_facts = inputs.get_generated_facts()
        self.assertEqual(1, len(generated_facts))
        self.assertEqual("be adapted", generated_facts[0].get_predicate().get())

    def test_are_not_alone(self):
        generated_fact = GeneratedFact("test", "are adapted", "nothing", "", False, 0.0, "")
        inputs = self.empty_input.add_generated_facts([generated_fact])
        inputs = self.be_normalization.process(inputs)
        generated_facts = inputs.get_generated_facts()
        self.assertEqual(1, len(generated_facts))
        self.assertEqual("be adapted", generated_facts[0].get_predicate().get())

    def test_were_not_alone(self):
        generated_fact = GeneratedFact("test", "were adapted", "nothing", "", False, 0.0, "")
        inputs = self.empty_input.add_generated_facts([generated_fact])
        inputs = self.be_normalization.process(inputs)
        generated_facts = inputs.get_generated_facts()
        self.assertEqual(1, len(generated_facts))
        self.assertEqual("was adapted", generated_facts[0].get_predicate().get())

    def test_no_change(self):
        generated_fact = GeneratedFact("test", "adapted", "nothing", "", False, 0.0, "")
        inputs = self.empty_input.add_generated_facts([generated_fact])
        inputs = self.be_normalization.process(inputs)
        generated_facts = inputs.get_generated_facts()
        self.assertEqual(1, len(generated_facts))
        self.assertEqual("adapted", generated_facts[0].get_predicate().get())


if __name__ == '__main__':
    unittest.main()
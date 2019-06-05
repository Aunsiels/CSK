import unittest

from quasimodo import Inputs
from quasimodo.filter_object_submodule import FilterObjectSubmodule
from quasimodo.generated_fact import GeneratedFact


class TestFilterObject(unittest.TestCase):

    def setUp(self) -> None:
        self.cleaning_predicate = FilterObjectSubmodule(None)
        self.empty_input = Inputs()

    def test_forbidden(self):
        generated_fact = GeneratedFact("test", "is", "used", "", False, 0.0, "")
        inputs = self.empty_input.add_generated_facts([generated_fact])
        inputs = self.cleaning_predicate.process(inputs)
        generated_facts = inputs.get_generated_facts()
        self.assertEqual(0, len(generated_facts))

    def test_totally_forbidden(self):
        generated_fact = GeneratedFact("test", "is", "useful minecraft", "", False, 0.0, "")
        inputs = self.empty_input.add_generated_facts([generated_fact])
        inputs = self.cleaning_predicate.process(inputs)
        generated_facts = inputs.get_generated_facts()
        self.assertEqual(0, len(generated_facts))

    def test_one_letter(self):
        generated_fact = GeneratedFact("test", "is", "a", "", False, 0.0, "")
        inputs = self.empty_input.add_generated_facts([generated_fact])
        inputs = self.cleaning_predicate.process(inputs)
        generated_facts = inputs.get_generated_facts()
        self.assertEqual(0, len(generated_facts))

    def test_dirty(self):
        generated_fact = GeneratedFact("test", "is", "their time", "", False, 0.0, "")
        inputs = self.empty_input.add_generated_facts([generated_fact])
        inputs = self.cleaning_predicate.process(inputs)
        generated_facts = inputs.get_generated_facts()
        self.assertEqual(1, len(generated_facts))
        self.assertEqual("time", generated_facts[0].get_object().get())

    def test_no_change(self):
        generated_fact = GeneratedFact("test", "is", "time", "", False, 0.0, "")
        inputs = self.empty_input.add_generated_facts([generated_fact])
        inputs = self.cleaning_predicate.process(inputs)
        generated_facts = inputs.get_generated_facts()
        self.assertEqual(1, len(generated_facts))
        self.assertEqual("time", generated_facts[0].get_object().get())


if __name__ == '__main__':
    unittest.main()

import unittest

from quasimodo import Inputs
from quasimodo.cleaning_predicate_submodule import CleaningPredicateSubmodule
from quasimodo.generated_fact import GeneratedFact


class TestCleaningPredicate(unittest.TestCase):

    def setUp(self) -> None:
        self.cleaning_predicate = CleaningPredicateSubmodule(None)
        self.empty_input = Inputs()

    def test_so(self):
        generated_fact = GeneratedFact("test", "is so", "nothing", "", False, 0.0, "")
        inputs = self.empty_input.add_generated_facts([generated_fact])
        inputs = self.cleaning_predicate.process(inputs)
        generated_facts = inputs.get_generated_facts()
        self.assertEqual(1, len(generated_facts))
        self.assertEqual("is", generated_facts[0].get_predicate().get())

    def test_xbox(self):
        generated_fact = GeneratedFact("test", "xbox", "nothing", "", False, 0.0, "")
        inputs = self.empty_input.add_generated_facts([generated_fact])
        inputs = self.cleaning_predicate.process(inputs)
        generated_facts = inputs.get_generated_facts()
        self.assertEqual(0, len(generated_facts))

    def test_no_change(self):
        generated_fact = GeneratedFact("test", "is", "nothing", "", False, 0.0, "")
        inputs = self.empty_input.add_generated_facts([generated_fact])
        inputs = self.cleaning_predicate.process(inputs)
        generated_facts = inputs.get_generated_facts()
        self.assertEqual(1, len(generated_facts))
        self.assertEqual("is", generated_facts[0].get_predicate().get())


if __name__ == '__main__':
    unittest.main()

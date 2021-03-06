import unittest

from quasimodo.assertion_normalization.cleaning_predicate_submodule import CleaningPredicateSubmodule
from quasimodo.data_structures.generated_fact import GeneratedFact
from quasimodo.data_structures.inputs import Inputs
from quasimodo.data_structures.multiple_source_occurrence import MultipleSourceOccurrence


class TestCleaningPredicate(unittest.TestCase):

    def setUp(self) -> None:
        self.cleaning_predicate = CleaningPredicateSubmodule(None)
        self.empty_input = Inputs()

    def test_so(self):
        generated_fact = GeneratedFact("test", "is so", "nothing", "", False, 0.0, MultipleSourceOccurrence())
        inputs = self.empty_input.add_generated_facts([generated_fact])
        inputs = self.cleaning_predicate.process(inputs)
        generated_facts = inputs.get_generated_facts()
        self.assertEqual(1, len(generated_facts))
        self.assertEqual("is", generated_facts[0].get_predicate().get())

    def test_xbox(self):
        generated_fact = GeneratedFact("test", "xbox", "nothing", "", False, 0.0, MultipleSourceOccurrence())
        inputs = self.empty_input.add_generated_facts([generated_fact])
        inputs = self.cleaning_predicate.process(inputs)
        generated_facts = inputs.get_generated_facts()
        self.assertEqual(0, len(generated_facts))

    def test_no_change(self):
        generated_fact = GeneratedFact("test", "is", "nothing", "", False, 0.0, MultipleSourceOccurrence())
        inputs = self.empty_input.add_generated_facts([generated_fact])
        inputs = self.cleaning_predicate.process(inputs)
        generated_facts = inputs.get_generated_facts()
        self.assertEqual(1, len(generated_facts))
        self.assertEqual("is", generated_facts[0].get_predicate().get())

    def test_no_verb(self):
        generated_fact = GeneratedFact("test", "table", "nothing", "", False, 0.0, MultipleSourceOccurrence())
        inputs = self.empty_input.add_generated_facts([generated_fact])
        inputs = self.cleaning_predicate.process(inputs)
        generated_facts = inputs.get_generated_facts()
        print(generated_facts)
        self.assertEqual(0, len(generated_facts))

    def test_no_verb2(self):
        generated_fact = GeneratedFact("wall", "clock", "yellow", "", False, 0.0, MultipleSourceOccurrence())
        inputs = self.empty_input.add_generated_facts([generated_fact])
        inputs = self.cleaning_predicate.process(inputs)
        generated_facts = inputs.get_generated_facts()
        print(generated_facts)
        self.assertEqual(0, len(generated_facts))

    def test_conjugated_verb(self):
        generated_fact = GeneratedFact("elephant", "going", "nowhere", "", False, 0.0, MultipleSourceOccurrence())
        inputs = self.empty_input.add_generated_facts([generated_fact])
        inputs = self.cleaning_predicate.process(inputs)
        generated_facts = inputs.get_generated_facts()
        self.assertEqual(1, len(generated_facts))

    def test_conjugated_verb2(self):
        generated_fact = GeneratedFact("elephant", "go", "nowhere", "", False, 0.0, MultipleSourceOccurrence())
        inputs = self.empty_input.add_generated_facts([generated_fact])
        inputs = self.cleaning_predicate.process(inputs)
        generated_facts = inputs.get_generated_facts()
        self.assertEqual(1, len(generated_facts))

    def test_conjugated_verb3(self):
        generated_fact = GeneratedFact("elephant", "goes", "nowhere", "", False, 0.0, MultipleSourceOccurrence())
        inputs = self.empty_input.add_generated_facts([generated_fact])
        inputs = self.cleaning_predicate.process(inputs)
        generated_facts = inputs.get_generated_facts()
        self.assertEqual(1, len(generated_facts))

    def test_not_digest(self):
        generated_fact = GeneratedFact("elephant", "not digests", "fruits", "",
                                       False, 0.0, MultipleSourceOccurrence())
        inputs = self.empty_input.add_generated_facts([generated_fact])
        inputs = self.cleaning_predicate.process(inputs)
        generated_facts = inputs.get_generated_facts()
        self.assertEqual(1, len(generated_facts))
        self.assertEqual(generated_facts[0].get_predicate().get(), "digests")
        self.assertTrue(generated_facts[0].is_negative())

    def test_empty_predicate(self):
        generated_fact = GeneratedFact("elephant", "", "fruits", "", False, 0.0, MultipleSourceOccurrence())
        inputs = self.empty_input.add_generated_facts([generated_fact])
        inputs = self.cleaning_predicate.process(inputs)
        generated_facts = inputs.get_generated_facts()
        self.assertEqual(0, len(generated_facts))

    def test_has_beach(self):
        generated_fact = GeneratedFact("beach", "has", "sand", "", False,
                                       0.0, MultipleSourceOccurrence())
        inputs = self.empty_input.add_generated_facts([generated_fact])
        inputs = self.cleaning_predicate.process(inputs)
        generated_facts = inputs.get_generated_facts()
        self.assertEqual(1, len(generated_facts))


if __name__ == '__main__':
    unittest.main()

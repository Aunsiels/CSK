import unittest

from quasimodo.fact_combinor import FactCombinor
from quasimodo.generated_fact import GeneratedFact
from quasimodo.inputs import Inputs
from quasimodo.multiple_scores import MultipleScore
from quasimodo.multiple_source_occurrence import MultipleSourceOccurrence
from quasimodo.openie_fact_generator_submodule import OpenIEFactGeneratorSubmodule
from quasimodo.referencable_interface import ReferencableInterface


class TestFactCombinor(unittest.TestCase):

    def setUp(self) -> None:
        dummy_reference = ReferencableInterface("Dummy reference")
        self.openie_fact_generator = OpenIEFactGeneratorSubmodule(dummy_reference)
        self.openie_fact_generator._name = "OPENIE"  # Dummy name only useful for testing
        self.empty_input = Inputs()

    def test_combination(self):
        score0 = MultipleScore()
        score0.add_score(1, None, None)
        score1 = MultipleScore()
        score1.add_score(0.5, None, None)
        score2 = MultipleScore()
        score2.add_score(0.7, None, None)
        generated_fact0 = GeneratedFact("lion", "eat", "zebra", "", False, score0,
                                        MultipleSourceOccurrence.from_raw("lions eat zebras", None, 1))
        mso = MultipleSourceOccurrence()
        mso.add_raw("lions eat zebras", None, 2)
        mso.add_raw("lions eat small zebras", None, 1)
        generated_fact1 = GeneratedFact("lion", "eat", "zebra", "", False, score1,
                                        mso)
        generated_fact2 = GeneratedFact("lion", "eat", "zebra", "", False, score2,
                                        MultipleSourceOccurrence.from_raw("lions eat small zebras", None, 1))
        new_gfs = [generated_fact0, generated_fact1, generated_fact2]
        inputs = self.empty_input.add_generated_facts(new_gfs)
        fact_combinor = FactCombinor(None)
        inputs = fact_combinor.process(inputs)
        self.assertEqual(1, len(inputs.get_generated_facts()))
        self.assertEqual(3, len(inputs.get_generated_facts()[0].get_score().scores))
        sentence = str(inputs.get_generated_facts()[0].get_sentence_source())
        self.assertIn("lions eat zebras", sentence)
        self.assertIn("lions eat small zebras", sentence)
        self.assertIn("x#x3", sentence)
        self.assertIn("x#x2", sentence)

    def test_combination_modalities(self):
        score0 = MultipleScore()
        score0.add_score(1, None, None)
        score1 = MultipleScore()
        score1.add_score(0.5, None, None)
        generated_fact0 = GeneratedFact("lion", "eat", "zebra", "some", False, score0, MultipleSourceOccurrence.from_raw("lions eat zebras", None, 1))
        generated_fact1 = GeneratedFact("lion", "eat", "zebra", "often", False, score1, MultipleSourceOccurrence.from_raw("lions eat zebras", None, 1))
        inputs = self.empty_input.add_generated_facts([generated_fact0, generated_fact1])
        fact_combinor = FactCombinor(None)
        inputs = fact_combinor.process(inputs)
        self.assertEqual(1, len(inputs.get_generated_facts()))
        self.assertIn("some", inputs.get_generated_facts()[0].get_modality().get())
        self.assertIn("often", inputs.get_generated_facts()[0].get_modality().get())


if __name__ == '__main__':
    unittest.main()

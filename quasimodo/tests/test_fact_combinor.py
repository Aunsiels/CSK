import unittest

from quasimodo.fact_combinor import FactCombinor
from quasimodo.data_structures.generated_fact import GeneratedFact
from quasimodo.data_structures.inputs import Inputs
from quasimodo.data_structures.multiple_scores import MultipleScore
from quasimodo.data_structures.multiple_source_occurrence import MultipleSourceOccurrence
from quasimodo.assertion_generation.openie_fact_generator_submodule import OpenIEFactGeneratorSubmodule
from quasimodo.data_structures.referencable_interface import ReferencableInterface


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

    def test_combination_modalities_tbc(self):
        score0 = MultipleScore()
        score0.add_score(1, None, None)
        score1 = MultipleScore()
        score1.add_score(0.5, None, None)
        generated_fact0 = GeneratedFact("parent", "have", "children",
                                        "TBC[many]",
                                        False,
                                        score0,
                                        MultipleSourceOccurrence.from_raw(
                                            "parents have many children", None,
                                            1))
        generated_fact1 = GeneratedFact("parent", "have", "children",
                                        "",
                                        False,
                                        score1,
                                        MultipleSourceOccurrence.from_raw(
                                            "parents have children", None, 1))
        inputs = self.empty_input.add_generated_facts([generated_fact0,
                                                       generated_fact1])
        fact_combinor = FactCombinor(None)
        inputs = fact_combinor.process(inputs)
        self.assertEqual(1, len(inputs.get_generated_facts()))
        self.assertIn("TBC[many]",
                      inputs.get_generated_facts()[0].get_modality().get())
        self.assertIn("parents have many children x#x1",
                      str(inputs.get_generated_facts()[
                              0].get_sentence_source()))
        self.assertIn("parents have children x#x1",
                      str(inputs.get_generated_facts()[
                              0].get_sentence_source()))

    def test_combination_modalities_long(self):
        score0 = MultipleScore()
        score0.add_score(1, None, None)
        score1 = MultipleScore()
        score1.add_score(0.5, None, None)
        generated_fact0 = GeneratedFact("parent", "go", "to Paris",
                                        "TBC[many]",
                                        False,
                                        score0,
                                        MultipleSourceOccurrence.from_raw(
                                            "parents have many children", None,
                                            1))
        generated_fact1 = GeneratedFact("parent", "go to", "Paris",
                                        "",
                                        False,
                                        score1,
                                        MultipleSourceOccurrence.from_raw(
                                            "parents have children", None, 1))
        inputs = self.empty_input.add_generated_facts([generated_fact0,
                                                       generated_fact1])
        fact_combinor = FactCombinor(None)
        inputs = fact_combinor.process(inputs)
        self.assertEqual(1, len(inputs.get_generated_facts()))
        self.assertIn("TBC[many]",
                      inputs.get_generated_facts()[0].get_modality().get())
        self.assertIn("parents have many children x#x1",
                      str(inputs.get_generated_facts()[
                              0].get_sentence_source()))
        self.assertIn("parents have children x#x1",
                      str(inputs.get_generated_facts()[
                              0].get_sentence_source()))
        self.assertEqual("go to",
                         inputs.get_generated_facts()[
                              0].get_predicate())

    def test_combination_modalities_long_fart(self):
        score0 = MultipleScore()
        score0.add_score(1, None, None)
        score1 = MultipleScore()
        score1.add_score(0.5, None, None)
        generated_fact0 = GeneratedFact("fart", "smell", "worse in shower",
                                        "always x#x9 // often x#x2",
                                        False,
                                        score0,
                                        MultipleSourceOccurrence.from_raw(
                                            "farts smell worse in the shower",
                                            None,
                                            1))
        generated_fact1 = GeneratedFact("fart", "smell worse in", "shower",
                                        "TBC[hot shower] x#x5 // always x#x1 // TBC[when shower] x#x1",
                                        False,
                                        score1,
                                        MultipleSourceOccurrence.from_raw(
                                            "farts smell worse in the shower", None, 1))
        inputs = self.empty_input.add_generated_facts([generated_fact0,
                                                       generated_fact1])
        fact_combinor = FactCombinor(None)
        inputs = fact_combinor.process(inputs)
        self.assertEqual(1, len(inputs.get_generated_facts()))
        self.assertIn("often",
                      inputs.get_generated_facts()[0].get_modality().get())
        self.assertIn("always x#x10",
                      inputs.get_generated_facts()[0].get_modality().get())
        self.assertEqual("smell worse in",
                         inputs.get_generated_facts()[
                              0].get_predicate())

    def test_beach(self):
        score0 = MultipleScore()
        score0.add_score(1, None, None)
        mso = MultipleSourceOccurrence()
        mso.add_raw("beaches have sand", "Google Autocomplete", 4)
        mso.add_raw("some beaches have sand", "Google Autocomplete", 2)
        mso.add_raw("some beaches have sand and some rocks", "Google "
                                                             "Autocomplete", 1)
        mso.add_raw("all beaches have sand", "Google Autocomplete", 4)
        mso.add_raw("beach have sand", "Google Autocomplete", 1)
        generated_fact0 = GeneratedFact("beach", "have", "sand",
                                        "some[subj/some] x#x3 // "
                                        "some[subj/all] x#x4",
                                        False,
                                        score0,
                                        mso)
        inputs = self.empty_input.add_generated_facts([generated_fact0])
        fact_combinor = FactCombinor(None)
        inputs = fact_combinor.process(inputs)
        self.assertEqual(1, len(inputs.get_generated_facts()))

    def test_combination_has_property(self):
        score0 = MultipleScore()
        score0.add_score(1, None, None)
        score1 = MultipleScore()
        score1.add_score(0.5, None, None)
        generated_fact0 = GeneratedFact("fart", "has_property", "in shower",
                                        "always x#x9 // often x#x2",
                                        False,
                                        score0,
                                        MultipleSourceOccurrence.from_raw(
                                            "farts are in shower",
                                            None,
                                            1))
        generated_fact1 = GeneratedFact("fart", "be in", "shower",
                                        "TBC[hot shower] x#x5 // always x#x1 // TBC[when shower] x#x1",
                                        False,
                                        score1,
                                        MultipleSourceOccurrence.from_raw(
                                            "farts smell worse in the shower", None, 1))
        inputs = self.empty_input.add_generated_facts([generated_fact0,
                                                       generated_fact1])
        fact_combinor = FactCombinor(None)
        inputs = fact_combinor.process(inputs)
        self.assertEqual(1, len(inputs.get_generated_facts()))
        self.assertEqual("be in",
                         inputs.get_generated_facts()[
                              0].get_predicate())


if __name__ == '__main__':
    unittest.main()

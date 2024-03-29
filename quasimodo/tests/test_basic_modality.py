import unittest

from quasimodo.assertion_normalization.basic_modality_submodule import \
    BasicModalitySubmodule
from quasimodo.data_structures.generated_fact import GeneratedFact
from quasimodo.data_structures.inputs import Inputs
from quasimodo.assertion_generation.openie_fact_generator_submodule import \
    OpenIEFactGeneratorSubmodule
from quasimodo.data_structures.multiple_scores import MultipleScore
from quasimodo.data_structures.multiple_source_occurrence import \
    MultipleSourceOccurrence
from quasimodo.data_structures.referencable_interface import \
    ReferencableInterface


class TestBasicModality(unittest.TestCase):

    def setUp(self) -> None:
        dummy_reference = ReferencableInterface("Dummy reference")
        self.openie_fact_generator = OpenIEFactGeneratorSubmodule(
            dummy_reference)
        self.openie_fact_generator._name = "OPENIE"  # Dummy name only useful for testing
        self.empty_input = Inputs()
        self.basic_modality = BasicModalitySubmodule(None)

    def test_always(self):
        suggestion = ("why does panda always climb tree", 1.0, None, "panda")
        new_gfs = self.openie_fact_generator.get_generated_facts([suggestion])
        inputs = self.empty_input.add_generated_facts(new_gfs)
        inputs = self.basic_modality.process(inputs)
        self.assertEqual(1, len(inputs.get_generated_facts()))
        self.assertEqual("panda",
                         inputs.get_generated_facts()[0].get_subject().get())
        self.assertEqual("climb",
                         inputs.get_generated_facts()[0].get_predicate().get())
        self.assertEqual("tree",
                         inputs.get_generated_facts()[0].get_object().get())
        self.assertIn("always",
                      inputs.get_generated_facts()[0].get_modality().get())

    def test_often_object(self):
        suggestion = ("why do pandas climb in tree often", 1.0, None, "panda")
        new_gfs = self.openie_fact_generator.get_generated_facts([suggestion])
        inputs = self.empty_input.add_generated_facts(new_gfs)
        inputs = self.basic_modality.process(inputs)
        self.assertEqual(1, len(inputs.get_generated_facts()))
        self.assertEqual("pandas",
                         inputs.get_generated_facts()[0].get_subject().get())
        self.assertEqual("climb in",
                         inputs.get_generated_facts()[0].get_predicate().get())
        self.assertEqual("tree",
                         inputs.get_generated_facts()[0].get_object().get())
        self.assertIn("often",
                      inputs.get_generated_facts()[0].get_modality().get())

    def test_with_already_one_modality(self):
        suggestion = (
            "why do african pandas eat bananas often", 1.0, None, "panda")
        new_gfs = self.openie_fact_generator.get_generated_facts([suggestion])
        inputs = self.empty_input.add_generated_facts(new_gfs)
        inputs = self.basic_modality.process(inputs)
        gfs = [x for x in inputs.get_generated_facts() if
               x.get_subject() == "pandas"]
        self.assertEqual(1, len(gfs))
        self.assertEqual("pandas", gfs[0].get_subject().get())
        self.assertEqual("eat", gfs[0].get_predicate().get())
        self.assertEqual("bananas", gfs[0].get_object().get())
        self.assertIn("often", gfs[0].get_modality().get())

    def test_multiple_sources(self):
        score = MultipleScore()
        score.add_score(1, None, None)
        mso = MultipleSourceOccurrence.from_raw(
                                           "parents have many children",
                                           "Google",
                                           10)
        print(mso)
        generated_fact = GeneratedFact("parent",
                                       "often have",
                                       "children",
                                       "TBC[many]",
                                       False,
                                       score,
                                       mso)
        inputs = self.empty_input.add_generated_facts([generated_fact])
        inputs = self.basic_modality.process(inputs)
        self.assertEqual(1, len(inputs.get_generated_facts()))
        print(inputs.get_generated_facts())
        self.assertIn("often x#x10",
                      inputs.get_generated_facts()[0].get_modality().get())


if __name__ == '__main__':
    unittest.main()

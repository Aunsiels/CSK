import unittest

from quasimodo import OpenIEFactGeneratorSubmodule, Inputs
from quasimodo.basic_modality_submodule import BasicModalitySubmodule
from quasimodo.referencable_interface import ReferencableInterface


class TestBasicModality(unittest.TestCase):

    def setUp(self) -> None:
        dummy_reference = ReferencableInterface("Dummy reference")
        self.openie_fact_generator = OpenIEFactGeneratorSubmodule(dummy_reference)
        self.openie_fact_generator._name = "OPENIE"  # Dummy name only useful for testing
        self.empty_input = Inputs()
        self.basic_modality = BasicModalitySubmodule(None)

    def test_always(self):
        suggestion = ("why does panda always climb tree", 1.0, None, "panda")
        new_gfs = self.openie_fact_generator.get_generated_facts([suggestion])
        inputs = self.empty_input.add_generated_facts(new_gfs)
        inputs = self.basic_modality.process(inputs)
        self.assertEqual(1, len(inputs.get_generated_facts()))
        self.assertEqual("panda", inputs.get_generated_facts()[0].get_subject().get())
        self.assertEqual("climb", inputs.get_generated_facts()[0].get_predicate().get())
        self.assertEqual("tree", inputs.get_generated_facts()[0].get_object().get())
        self.assertIn("always", inputs.get_generated_facts()[0].get_modality().get())

    def test_often_object(self):
        suggestion = ("why do pandas climb in tree often", 1.0, None, "panda")
        new_gfs = self.openie_fact_generator.get_generated_facts([suggestion])
        inputs = self.empty_input.add_generated_facts(new_gfs)
        inputs = self.basic_modality.process(inputs)
        self.assertEqual(1, len(inputs.get_generated_facts()))
        self.assertEqual("pandas", inputs.get_generated_facts()[0].get_subject().get())
        self.assertEqual("climb in", inputs.get_generated_facts()[0].get_predicate().get())
        self.assertEqual("tree", inputs.get_generated_facts()[0].get_object().get())
        self.assertIn("often", inputs.get_generated_facts()[0].get_modality().get())


if __name__ == '__main__':
    unittest.main()

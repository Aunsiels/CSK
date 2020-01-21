import unittest

from quasimodo.data_structures.inputs import Inputs
from quasimodo.assertion_generation.quora_questions_submodule import QuoraQuestionsSubmodule
from quasimodo.data_structures.subject import Subject


class TestQuora(unittest.TestCase):

    def setUp(self) -> None:
        self.quora = QuoraQuestionsSubmodule(None)
        self.empty_input = Inputs()

    def test_elephant(self):
        inputs = self.empty_input.add_subjects({Subject("elephant")})
        inputs = self.quora.process(inputs)
        generated_facts = inputs.get_generated_facts()
        self.assertEqual(1, len(generated_facts))
        self.assertIn("elephant", generated_facts[0].get_subject().get())
        self.assertTrue(generated_facts[0].is_negative())
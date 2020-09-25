import unittest

from quasimodo.assertion_validation.perplexity_submodule import \
    PerplexitySubmodule
from quasimodo.data_structures.generated_fact import GeneratedFact
from quasimodo.data_structures.inputs import Inputs
from quasimodo.data_structures.multiple_scores import MultipleScore
from quasimodo.data_structures.multiple_source_occurrence import \
    MultipleSourceOccurrence


class TestPerplexity(unittest.TestCase):

    def test_simple(self):
        score = MultipleScore()
        generated_fact = GeneratedFact(
            "cat",
            "love",
            "catnip",
            "",
            False,
            score,
            MultipleSourceOccurrence.from_raw("cats love catnip", None, 1))
        submodule = PerplexitySubmodule(None)
        empty_input = Inputs()
        inputs = empty_input.add_generated_facts([generated_fact])
        inputs = submodule.process(inputs)
        new_gfs = inputs.get_generated_facts()
        self.assertEqual(len(new_gfs), 1)
        self.assertEqual(1,
                         len(inputs.get_generated_facts()[0].get_score(
                         ).scores))
        self.assertLessEqual(
            inputs.get_generated_facts()[0].get_score().scores[0][0],
            0.5)

    def test_nothing(self):
        score = MultipleScore()
        generated_fact = GeneratedFact(
            "cat",
            "love",
            "catnip",
            "",
            False,
            score,
            MultipleSourceOccurrence.from_raw("cats lovessz catnip", None, 1))
        submodule = PerplexitySubmodule(None)
        empty_input = Inputs()
        inputs = empty_input.add_generated_facts([generated_fact])
        inputs = submodule.process(inputs)
        new_gfs = inputs.get_generated_facts()
        self.assertEqual(len(new_gfs), 1)
        self.assertEqual(0,
                         len(inputs.get_generated_facts()[0].get_score(
                         ).scores))

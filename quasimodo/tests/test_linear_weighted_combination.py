import unittest

from quasimodo.inputs import Inputs
from quasimodo.bing_autocomplete_submodule import BingAutocompleteSubmodule
from quasimodo.generated_fact import GeneratedFact
from quasimodo.google_autocomplete_submodule import GoogleAutocompleteSubmodule
from quasimodo.linear_combination_weighted_submodule import LinearCombinationWeightedSubmodule
from quasimodo.multiple_scores import MultipleScore
from quasimodo.referencable_interface import ReferencableInterface


class TestLinearWeightedCombination(unittest.TestCase):

    def setUp(self) -> None:
        self.dummy_reference = ReferencableInterface("Dummy reference")
        self.linear_combination = LinearCombinationWeightedSubmodule(self.dummy_reference)
        self.empty_input = Inputs()

    def test_combination(self):
        dataset = [("elephant", "download", "baby", 0), ("elephant", "climb", "trunk", 0),
                   ("elephant", "bear", "baby", 1), ("elephant", "download this cute illustration with", "baby", 0),
                   ("elephant", "be", "ear", 0), ("elephant", "fry", "ear", 0), ("elephant", "trek", "travel", 0),
                   ("elephant", "forbid love in", "water", 0), ("elephant", "eat", "bark", 1),
                   ("elephant", "have", "tusks", 1)]
        gfs = []
        pos = 0
        for subject, predicate, obj, truth in dataset:
            pos += 1
            score = MultipleScore()
            if pos%2 == 0:
                score.add_score(truth, self.dummy_reference, GoogleAutocompleteSubmodule(self.dummy_reference))
            else:
                score.add_score(truth, self.dummy_reference, BingAutocompleteSubmodule(self.dummy_reference))
            gfs.append(GeneratedFact(subject, predicate, obj, "", False, score, ""))
        score2 = MultipleScore()
        score2.add_score(1, self.dummy_reference, GoogleAutocompleteSubmodule(self.dummy_reference))
        gfs.append(GeneratedFact("elephant", "be", "big", "", False, score2, "elephants are big"))
        inputs = self.empty_input.add_generated_facts(gfs)
        inputs = self.linear_combination.process(inputs)
        self.assertEqual(len(dataset) + 1, len(inputs.get_generated_facts()))
        self.assertTrue(False)


if __name__ == '__main__':
    unittest.main()

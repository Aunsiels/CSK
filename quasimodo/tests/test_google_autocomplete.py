import unittest

from quasimodo.assertion_normalization.cleaning_predicate_submodule import \
    CleaningPredicateSubmodule
from quasimodo.data_structures.inputs import Inputs
from quasimodo.assertion_generation.google_autocomplete_submodule import GoogleAutocompleteSubmodule
from quasimodo.patterns.pattern_google import PatternGoogle
from quasimodo.data_structures.subject import Subject


class TestGoogleAutocomplete(unittest.TestCase):

    def setUp(self) -> None:
        self.autocomplete = GoogleAutocompleteSubmodule(None, use_cache=False)
        self.autocomplete_cache = GoogleAutocompleteSubmodule(None, use_cache=True, cache_name="google-cache-test")
        self.empty_input = Inputs()

    def test_elephant(self):
        suggestions, from_cache = self.autocomplete.get_suggestion("why are elephants")
        self.assertFalse(from_cache)
        self.assertEqual(len(suggestions), 10)

    def test_cache(self):
        _, _ = self.autocomplete_cache.get_suggestion("why are elephants")
        # Remove information of the previous query
        self.autocomplete_cache.local_cache["query_regex"] = ""
        suggestions, from_cache = self.autocomplete_cache.get_suggestion("why are elephants")
        self.assertTrue(from_cache)
        self.assertEqual(len(suggestions), 10)
        self.autocomplete_cache.cache.delete_cache()

    def test_process(self):
        inputs = self.empty_input.add_subjects([Subject("elephant")]).add_patterns([PatternGoogle("why are <SUBJS>")])
        inputs = self.autocomplete.process(inputs)
        self.assertTrue(len(inputs.get_generated_facts()) > 20)
        trunk_facts = [x for x in inputs.get_generated_facts() if "trunk" in x.get_object().get()]
        self.assertTrue(len(trunk_facts) > 0)

    def test_vegetarian_negative_pattern(self):
        inputs = self.empty_input.add_subjects(
            [Subject("vegetarian")]).add_patterns(
            [PatternGoogle("why don't <SUBJS>", negative=True)])
        inputs = self.autocomplete.process(inputs)
        self.assertTrue(len(inputs.get_generated_facts()) > 0)
        meat_facts = [x for x in inputs.get_generated_facts() if
                       "meat" == x.get_object().get() and
                       not x.is_negative()
                      ]
        print(meat_facts)
        self.assertTrue(len(meat_facts) == 0)

    def test_vegetarian_positive_pattern(self):
        inputs = self.empty_input.add_subjects(
            [Subject("vegetarian")]).add_patterns(
            [PatternGoogle("why do <SUBJS>")])
        inputs = self.autocomplete.process(inputs)
        predicate_cleaning = CleaningPredicateSubmodule(None)
        inputs = predicate_cleaning.process(inputs)
        self.assertTrue(len(inputs.get_generated_facts()) > 0)
        meat_facts = [x for x in inputs.get_generated_facts() if
                       "meat" == x.get_object().get() and
                       not x.is_negative()
                      ]
        self.assertTrue(len(meat_facts) > 0)


if __name__ == '__main__':
    unittest.main()

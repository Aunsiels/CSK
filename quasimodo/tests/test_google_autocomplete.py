import unittest

from quasimodo import Inputs, PatternGoogle
from quasimodo.google_autocomplete_submodule import GoogleAutocompleteSubmodule
from quasimodo.subject import Subject


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


if __name__ == '__main__':
    unittest.main()

import time
import unittest

from quasimodo.assertion_generation.bing_autocomplete_submodule import BingAutocompleteSubmodule
from quasimodo.data_structures.inputs import Inputs
from quasimodo.patterns.pattern_google import PatternGoogle
from quasimodo.data_structures.subject import Subject


class TestBingAutocomplete(unittest.TestCase):

    def setUp(self) -> None:
        self.autocomplete = BingAutocompleteSubmodule(None, use_cache=False, look_new=True)
        self.autocomplete_cache = BingAutocompleteSubmodule(None, use_cache=True,
                                                            cache_name="google-cache-test", look_new=True)
        self.empty_input = Inputs()

    def test_elephant(self):
        suggestions, from_cache = self.autocomplete.get_suggestion("why are elephants")
        self.assertFalse(from_cache)
        self.assertEqual(len(suggestions), 8)

    def test_cache(self):
        _, _ = self.autocomplete_cache.get_suggestion("why are elephants")
        time.sleep(10)
        suggestions, from_cache = self.autocomplete_cache.get_suggestion("why are elephants")
        self.assertTrue(from_cache)
        self.assertEqual(len(suggestions), 8)
        self.autocomplete_cache.cache.delete_cache()

    def _test_process(self):
        inputs = self.empty_input.add_subjects([Subject("elephant")]).add_patterns([PatternGoogle("why are <SUBJS>")])
        inputs = self.autocomplete.process(inputs)
        self.assertTrue(len(inputs.get_generated_facts()) > 16)
        trunk_facts = [x for x in inputs.get_generated_facts() if "trunk" in x.get_object().get()]
        self.assertTrue(len(trunk_facts) > 0)


if __name__ == '__main__':
    unittest.main()

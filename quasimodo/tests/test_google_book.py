import unittest

from quasimodo.inputs import Inputs
from quasimodo.generated_fact import GeneratedFact
from quasimodo.google_book_submodule import GoogleBookSubmodule
from quasimodo.multiple_scores import MultipleScore
from quasimodo.multiple_source_occurrence import MultipleSourceOccurrence


class TestGoogleBook(unittest.TestCase):

    def setUp(self) -> None:
        self.google_book_no_cache = GoogleBookSubmodule(None, False)
        self.empty_input = Inputs()

    def test_lion_eat_zebras(self):
        generated_fact = GeneratedFact("lion", "eat", "zebra", "", False, MultipleScore(), MultipleSourceOccurrence())
        inputs = self.empty_input.add_generated_facts([generated_fact])
        inputs = self.google_book_no_cache.process(inputs)
        self.assertEqual(1, len(inputs.get_generated_facts()))
        scores = inputs.get_generated_facts()[0].get_score()
        scores_google_book = [x for x in scores.scores if x[2].get_name() == "Google Book Submodule"]
        self.assertEqual(1, len(scores_google_book))
        self.assertTrue(scores_google_book[0][0] != 0)

    def test_lion_eat_code(self):
        generated_fact = GeneratedFact("lion", "eat", "code", "", False, MultipleScore(), MultipleSourceOccurrence())
        inputs = self.empty_input.add_generated_facts([generated_fact])
        inputs = self.google_book_no_cache.process(inputs)
        self.assertEqual(1, len(inputs.get_generated_facts()))
        scores = inputs.get_generated_facts()[0].get_score()
        scores_google_book = [x for x in scores.scores if x[2].get_name() == "Google Book Submodule"]
        self.assertEqual(1, len(scores_google_book))
        self.assertTrue(scores_google_book[0][0] == 0)

    def test_cache(self):
        google_book_cache = GoogleBookSubmodule(None, True, cache_name="google-book-cache-temp")
        generated_fact = GeneratedFact("lion", "eat", "zebra", "", False, MultipleScore(), MultipleSourceOccurrence())
        inputs = self.empty_input.add_generated_facts([generated_fact])
        google_book_cache.process(inputs)
        generated_fact = GeneratedFact("lion", "eat", "zebra", "", False, MultipleScore(), MultipleSourceOccurrence())
        inputs = self.empty_input.add_generated_facts([generated_fact])
        inputs = google_book_cache.process(inputs)
        self.assertEqual(1, len(inputs.get_generated_facts()))
        scores = inputs.get_generated_facts()[0].get_score()
        scores_google_book = [x for x in scores.scores if x[2].get_name() == "Google Book Submodule"]
        self.assertEqual(1, len(scores_google_book))
        self.assertTrue(scores_google_book[0][0] != 0)
        google_book_cache.cache.delete_cache()


if __name__ == '__main__':
    unittest.main()

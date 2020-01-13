import unittest

from quasimodo.generated_fact import GeneratedFact
from quasimodo.inputs import Inputs
from quasimodo.multiple_source_occurrence import MultipleSourceOccurrence
from quasimodo.similar_object_remover import SimilarObjectRemover


class TestSimilarObjectRemover(unittest.TestCase):

    def test_article(self):
        gfs = [GeneratedFact("bee", "make", "hive", "", False, 0.1, MultipleSourceOccurrence()),
               GeneratedFact("bee", "make", "a hive", "", False, 0.1, MultipleSourceOccurrence())]
        inputs = Inputs()
        inputs = inputs.add_generated_facts(gfs)
        remover = SimilarObjectRemover(None)
        inputs = remover.process(inputs)
        self.assertEqual(len(inputs.get_generated_facts()), 2)
        self.assertEqual(len(set([x.get_object().get() for x in inputs.get_generated_facts()])), 1)

    def test_plural(self):
        gfs = [GeneratedFact("bee", "make", "hive", "", False, 0.1, MultipleSourceOccurrence()),
               GeneratedFact("bee", "make", "hives", "", False, 0.1, MultipleSourceOccurrence())]
        inputs = Inputs()
        inputs = inputs.add_generated_facts(gfs)
        remover = SimilarObjectRemover(None)
        inputs = remover.process(inputs)
        self.assertEqual(len(inputs.get_generated_facts()), 2)
        self.assertEqual(len(set([x.get_object().get() for x in inputs.get_generated_facts()])), 1)

    def test_plural_and_article(self):
        gfs = [GeneratedFact("bee", "make", "hive", "", False, 0.1, MultipleSourceOccurrence()),
               GeneratedFact("bee", "make", "the hives", "", False, 0.1, MultipleSourceOccurrence())]
        inputs = Inputs()
        inputs = inputs.add_generated_facts(gfs)
        remover = SimilarObjectRemover(None)
        inputs = remover.process(inputs)
        self.assertEqual(len(inputs.get_generated_facts()), 2)
        self.assertEqual(len(set([x.get_object().get() for x in inputs.get_generated_facts()])), 1)


if __name__ == '__main__':
    unittest.main()

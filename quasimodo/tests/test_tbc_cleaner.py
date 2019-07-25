import unittest

from quasimodo.generated_fact import GeneratedFact
from quasimodo.inputs import Inputs
from quasimodo.multiple_scores import MultipleScore
from quasimodo.tbc_cleaner import TBCCleaner


class TestTBCCleaner(unittest.TestCase):

    def test_remove(self):
        inputs = Inputs()
        gfs = [GeneratedFact("elephant", "eat", "bananas", "TBC[big bananas]", 0, MultipleScore(),
                             "elephants eat big bananas")]
        inputs = inputs.add_generated_facts(gfs)
        tbc_cleaner = TBCCleaner(None)
        inputs = tbc_cleaner.process(inputs)
        self.assertEqual(len(inputs.get_generated_facts()), 0)

    def test_remove2(self):
        inputs = Inputs()
        gfs = [GeneratedFact("elephant", "eat", "bananas", "TBC[big bananas] x#x2", 0, MultipleScore(),
                             "elephants eat big bananas x#x2")]
        inputs = inputs.add_generated_facts(gfs)
        tbc_cleaner = TBCCleaner(None)
        inputs = tbc_cleaner.process(inputs)
        self.assertEqual(len(inputs.get_generated_facts()), 0)

    def test_remove3(self):
        inputs = Inputs()
        gfs = [GeneratedFact("elephant", "eat", "bananas", "TBC[big bananas] x#x2", 0, MultipleScore(),
                             "elephants eat big bananas // elephants eat big and fat bananas")]
        inputs = inputs.add_generated_facts(gfs)
        tbc_cleaner = TBCCleaner(None)
        inputs = tbc_cleaner.process(inputs)
        self.assertEqual(len(inputs.get_generated_facts()), 0)

    def test_not_remove(self):
        inputs = Inputs()
        gfs = [GeneratedFact("elephant", "eat", "bananas", "TBC[big bananas]", 0, MultipleScore(),
                             "elephants eat big bananas x#x2")]
        inputs = inputs.add_generated_facts(gfs)
        tbc_cleaner = TBCCleaner(None)
        inputs = tbc_cleaner.process(inputs)
        self.assertEqual(len(inputs.get_generated_facts()), 1)

    def test_not_remove2(self):
        inputs = Inputs()
        gfs = [GeneratedFact("elephant", "eat", "bananas", "TBC[big bananas] // TBC[small bananas]", 0, MultipleScore(),
                             "elephants eat big bananas // elephants eat small bananas")]
        inputs = inputs.add_generated_facts(gfs)
        tbc_cleaner = TBCCleaner(None)
        inputs = tbc_cleaner.process(inputs)
        self.assertEqual(len(inputs.get_generated_facts()), 1)


if __name__ == '__main__':
    unittest.main()

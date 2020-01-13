import unittest

from quasimodo.generated_fact import GeneratedFact
from quasimodo.inputs import Inputs
from quasimodo.multiple_scores import MultipleScore
from quasimodo.multiple_source_occurrence import MultipleSourceOccurrence
from quasimodo.tbc_cleaner import TBCCleaner


class TestTBCCleaner(unittest.TestCase):

    def test_remove(self):
        inputs = Inputs()
        mso = MultipleSourceOccurrence()
        mso.add_raw("elephants eat big bananas", None, 1)
        gfs = [GeneratedFact("elephant", "eat", "bananas", "TBC[big bananas]", 0, MultipleScore(),
                             mso)]
        inputs = inputs.add_generated_facts(gfs)
        tbc_cleaner = TBCCleaner(None)
        inputs = tbc_cleaner.process(inputs)
        self.assertEqual(len(inputs.get_generated_facts()), 0)

    def test_remove2(self):
        inputs = Inputs()
        mso = MultipleSourceOccurrence()
        mso.add_raw("elephants eat big bananas", None, 2)
        gfs = [GeneratedFact("elephant", "eat", "bananas", "TBC[big bananas] x#x2", 0, MultipleScore(),
                             mso)]
        inputs = inputs.add_generated_facts(gfs)
        tbc_cleaner = TBCCleaner(None)
        inputs = tbc_cleaner.process(inputs)
        self.assertEqual(len(inputs.get_generated_facts()), 0)

    def test_remove3(self):
        inputs = Inputs()
        mso = MultipleSourceOccurrence()
        mso.add_raw("elephants eat big bananas", None, 1)
        mso.add_raw("elephants eat big and fat bananas", None, 1)
        gfs = [GeneratedFact("elephant", "eat", "bananas", "TBC[big bananas] x#x2", 0, MultipleScore(),
                             mso)]
        inputs = inputs.add_generated_facts(gfs)
        tbc_cleaner = TBCCleaner(None)
        inputs = tbc_cleaner.process(inputs)
        self.assertEqual(len(inputs.get_generated_facts()), 0)

    def test_not_remove(self):
        inputs = Inputs()
        mso = MultipleSourceOccurrence()
        mso.add_raw("elephants eat big bananas", None, 2)
        gfs = [GeneratedFact("elephant", "eat", "bananas", "TBC[big bananas]", 0, MultipleScore(),
                             mso)]
        inputs = inputs.add_generated_facts(gfs)
        tbc_cleaner = TBCCleaner(None)
        inputs = tbc_cleaner.process(inputs)
        self.assertEqual(len(inputs.get_generated_facts()), 1)

    def test_not_remove2(self):
        inputs = Inputs()
        mso = MultipleSourceOccurrence()
        mso.add_raw("elephants eat big bananas", None, 1)
        mso.add_raw("elephants eat small bananas", None, 1)
        gfs = [GeneratedFact("elephant", "eat", "bananas", "TBC[big bananas] // TBC[small bananas]", 0, MultipleScore(),
                             mso)]
        inputs = inputs.add_generated_facts(gfs)
        tbc_cleaner = TBCCleaner(None)
        inputs = tbc_cleaner.process(inputs)
        self.assertEqual(len(inputs.get_generated_facts()), 1)


if __name__ == '__main__':
    unittest.main()

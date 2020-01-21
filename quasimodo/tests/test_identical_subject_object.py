import unittest

from quasimodo.data_structures.inputs import Inputs
from quasimodo.data_structures.generated_fact import GeneratedFact
from quasimodo.assertion_normalization.identical_subject_object_submodule import IdenticalSubjectObjectSubmodule
from quasimodo.data_structures.multiple_source_occurrence import MultipleSourceOccurrence


class TestIdenticalSubjectObject(unittest.TestCase):

    def setUp(self) -> None:
        self.identical = IdenticalSubjectObjectSubmodule(None)
        self.empty_input = Inputs()

    def test_removal(self):
        new_gfs = [GeneratedFact("lion", "eat", "lion", "some", False, None, MultipleSourceOccurrence())]
        inputs = self.empty_input.replace_generated_facts(new_gfs)
        inputs = self.identical.process(inputs)
        self.assertEqual(0, len(inputs.get_generated_facts()))


if __name__ == '__main__':
    unittest.main()

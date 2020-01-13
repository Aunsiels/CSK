import unittest

from quasimodo.inputs import Inputs
from quasimodo.generated_fact import GeneratedFact
from quasimodo.identical_subject_object_submodule import IdenticalSubjectObjectSubmodule
from quasimodo.multiple_source_occurrence import MultipleSourceOccurrence


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

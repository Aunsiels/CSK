import unittest

from quasimodo.seeds.all_seeds_module import AllSeedsModule
from quasimodo.data_structures.inputs import Inputs


class TestAllSeeds(unittest.TestCase):

    def setUp(self):
        self.all_seeds_module = AllSeedsModule()
        empty_input = Inputs()
        self.inputs = self.all_seeds_module.process(empty_input)

    def test_contains_animal(self):
        self.assertIn("worm", self.inputs.get_subjects())

    def test_contains_occupation(self):
        self.assertIn("doctor", self.inputs.get_subjects())

    def test_contains_noun(self):
        self.assertIn("pen", self.inputs.get_subjects())

    def test_subject_removal(self):
        self.assertNotIn("it", self.inputs.get_subjects())


if __name__ == '__main__':
    unittest.main()

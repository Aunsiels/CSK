import unittest

from quasimodo import AnimalSubmodule, Inputs
from quasimodo.animal_seed_module import AnimalSeedModule


class TestAnimalSubmodule(unittest.TestCase):

    def setUp(self) -> None:
        self.animal_submodule = AnimalSubmodule(None)
        self.animal_module = AnimalSeedModule()
        self.empty_input_interface = Inputs()

    def test_something(self):
        animal_input_interface = self.animal_submodule.process(self.empty_input_interface)
        self.assertIn("worm", animal_input_interface.get_subjects())

    def test_animal_module(self):
        animal_input_interface = self.animal_module.process(self.empty_input_interface)
        self.assertIn("worm", animal_input_interface.get_subjects())


if __name__ == '__main__':
    unittest.main()

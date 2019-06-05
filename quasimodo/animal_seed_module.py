from .module_interface import ModuleInterface
from .default_submodule_factory import DefaultSubmoduleFactory
import logging

class AnimalSeedModule(ModuleInterface):
    """AnimalSeedModule
    A module which only produced subjects which are animals and nothing else
    """

    def __init__(self):
        module_names = ["animal-seeds"]
        super(AnimalSeedModule, self).__init__(
            module_names, DefaultSubmoduleFactory())
        self._name = "Animal Seed module"

    def process(self, input_interface):
        logging.info("Generate animal seeds")
        return self._submodules[0].process(input_interface)

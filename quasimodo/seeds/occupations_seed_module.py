from quasimodo.data_structures.module_interface import ModuleInterface
from quasimodo.default_submodule_factory import DefaultSubmoduleFactory
import logging


class OccupationsSeedModule(ModuleInterface):

    def __init__(self):
        module_names = ["occupations-seeds"]
        super(OccupationsSeedModule, self).__init__(
            module_names, DefaultSubmoduleFactory())
        self._name = "Occupation module"

    def process(self, input_interface):
        logging.info("Generate occupations seeds")
        return self._submodules[0].process(input_interface)

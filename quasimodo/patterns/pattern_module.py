from quasimodo.data_structures.module_interface import ModuleInterface
from quasimodo.default_submodule_factory import DefaultSubmoduleFactory
from quasimodo.data_structures.inputs import Inputs
import logging


class PatternModule(ModuleInterface):
    """PatternModule
    Module which generates patterns
    """

    def __init__(self):
        module_names = ["manual-patterns-google"]
        super(PatternModule, self).__init__(
            module_names, DefaultSubmoduleFactory())
        self._name = "Pattern Module"

    def process(self, input_interface):
        logging.info("Start the Pattern Generation module")
        new_inputs = []
        for submodule in self._submodules:
            new_inputs.append(submodule.process(input_interface))
        new_patterns = input_interface.get_patterns()
        for inputs in new_inputs:
            new_patterns += inputs.get_patterns()
        return Inputs(input_interface.get_seeds(),
                      new_patterns,
                      input_interface.get_generated_facts(),
                      input_interface.get_subjects(),
                      input_interface.get_objects())

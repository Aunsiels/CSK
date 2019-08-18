from .module_interface import ModuleInterface
from .default_submodule_factory import DefaultSubmoduleFactory
import logging


class OutputModule(ModuleInterface):

    def __init__(self):
        module_names = ["tsv-output", "statistics"]
        super(OutputModule, self).__init__(
            module_names, DefaultSubmoduleFactory())
        self._name = "Output Module"

    def process(self, input_interface):
        logging.info("Start the output module")
        for submodule in self._submodules:
            input_interface = submodule.process(input_interface)
        return input_interface

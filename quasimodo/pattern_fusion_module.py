from .module_interface import ModuleInterface
from .default_submodule_factory import DefaultSubmoduleFactory
import logging


class PatternFusionModule(ModuleInterface):
    """PatternFusionModule
    Module used to merge patterns coming from different sources
    """

    def __init__(self):
        module_names = []
        super(PatternFusionModule, self).__init__(
            module_names, DefaultSubmoduleFactory())
        self._name = "Pattern Fusion Module"

    def process(self, input_interface):
        # Nothing for now
        logging.info("Start the pattern fusion module")
        return input_interface

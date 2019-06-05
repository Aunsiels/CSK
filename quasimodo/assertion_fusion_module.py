from .module_interface import ModuleInterface
from .default_submodule_factory import DefaultSubmoduleFactory
import logging


class AssertionFusionModule(ModuleInterface):
    """AssertionFusionModule
    A module which combines the assertions coming from several sources
    """

    def __init__(self):
        module_names = ["linear-combination-weighted",
                        ]
        super(AssertionFusionModule, self).__init__(
            module_names, DefaultSubmoduleFactory())
        self._name = "Assertion Fusion Module"

    def process(self, input_interface):
        logging.info("Start the assertion fusion module")
        for submodule in self._submodules:
            input_interface = submodule.process(input_interface)
        return input_interface

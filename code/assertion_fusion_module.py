from module_interface import ModuleInterface
from default_submodule_factory import DefaultSubmoduleFactory
from inputs import Inputs

class AssertionFusionModule(ModuleInterface):
    """AssertionFusionModule
    A module which combines the assertions coming from several sources
    """

    def __init__(self):
        module_names = []
        super(AssertionFusionModule, self).__init__(
            module_names, DefaultSubmoduleFactory())
        self._name = "Assertion Fusion Module"

    def process(self, input_interface):
        # Nothing for now
        return input_interface

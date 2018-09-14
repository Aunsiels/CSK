from module_interface import ModuleInterface
from default_submodule_factory import DefaultSubmoduleFactory
from inputs import Inputs

class AssertionValidationModule(ModuleInterface):
    """AssertionValidationModule
    A module which valides assertions, i.e. given an assertion, give a new score
    to it.
    """

    def __init__(self):
        module_names = []
        super(AssertionValidationModule, self).__init__(
            module_names, DefaultSubmoduleFactory())
        self._name = "Assertion Validation Module"

    def process(self, input_interface):
        # Nothing for now
        return input_interface

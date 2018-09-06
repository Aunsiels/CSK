from module_reference_interface import ModuleReferenceInterface
from process_interface import ProcessInterface

class ModuleInterface(ModuleReferenceInterface, ProcessInterface):
    """ModuleInterface
    Represents a module
    """

    def __init__(self):
        self._submodules = []

    def get_submodules(self, submodule_factory):
        raise NotImplementedError

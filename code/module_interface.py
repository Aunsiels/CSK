from module_reference_interface import ModuleReferenceInterface
from process_interface import ProcessInterface

class ModuleInterface(ModuleReferenceInterface, ProcessInterface):
    """ModuleInterface
    Represents a module
    """

    def __init__(self, submodules_names, submodules_factory):
        self._submodules = []
        # The submodules names are used during the generation of the submodules
        # The order is conserved
        self._submodules_names = submodules_names
        # To create the submodules
        self._submodules_factory = submodules_factory
        # Initialize the submodules
        self._submodules = self._get_submodules()

    def _get_submodules(self):
        """get_submodules
        Generates the submodules of this module
        :return: the submodules
        :rtype: List[SubmoduleInterface]
        """
        submodules = []
        for name in self._submodules_names:
            submodules.append(self._submodules_factory.get_submodule(name,
                                                                     self))
        return submodules

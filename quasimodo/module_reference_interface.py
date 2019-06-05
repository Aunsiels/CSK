from .referencable_interface import ReferencableInterface


class ModuleReferenceInterface(ReferencableInterface):
    """ModuleReferenceInterface
    Represents a reference to a module
    """

    def __init__(self, name):
        super().__init__(name)

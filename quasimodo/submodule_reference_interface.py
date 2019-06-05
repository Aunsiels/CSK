from .referencable_interface import ReferencableInterface


class SubmoduleReferenceInterface(ReferencableInterface):
    """SubmoduleReferenceInterface
    Represents a reference to a submodule
    """

    def __init__(self, name):
        super().__init__(name)

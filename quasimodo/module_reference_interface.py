from quasimodo.serializable import Serializable
from .referencable_interface import ReferencableInterface


class ModuleReferenceInterface(ReferencableInterface, Serializable):
    """ModuleReferenceInterface
    Represents a reference to a module
    """

    def to_dict(self):
        res = dict()
        res["type"] = "ModuleReference"
        res["name"] = self.get_name()
        return res

    def __init__(self, name):
        super().__init__(name)

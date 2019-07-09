from quasimodo.serializable import Serializable
from .referencable_interface import ReferencableInterface


class SubmoduleReferenceInterface(ReferencableInterface, Serializable):
    """SubmoduleReferenceInterface
    Represents a reference to a submodule
    """

    def to_dict(self):
        res = dict()
        res["type"] = "SubmoduleReference"
        res["name"] = self.get_name()
        return res

    def __init__(self, name):
        super().__init__(name)

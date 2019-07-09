from quasimodo.serializable import Serializable
from .object_interface import ObjectInterface


class Object(ObjectInterface, Serializable):
    """Object
    The default implementation of the ObjectInterface
    """

    def to_dict(self):
        res = dict()
        res["type"] = "Object"
        res["value"] = self.get()
        return res

    def __init__(self, obj):
        super().__init__()
        self._object = obj

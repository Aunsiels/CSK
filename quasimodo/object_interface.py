from .spom_interface import SPOMInterface


class ObjectInterface(SPOMInterface):
    """ObjectInterface
    Represents a object
    """

    def __init__(self):
        self._object = ""

    def get(self):
        return self._object

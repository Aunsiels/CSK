from object_interface import ObjectInterface

class Object(ObjectInterface):
    """Object
    The default implementation of the ObjectInterface
    """

    def __init__(self, obj):
        self._object = obj

class ReferencableInterface(object):
    """ReferencableInterface
    Represents something which can be refered
    """

    def __init__(self, name):
        self._name = name

    def get_name(self):
        """get_name
        Gives the name of the module
        """
        return self._name

    def __str__(self):
        return "Reference(" + str(self.get_name()) + ")"

    def __hash__(self):
        return hash(self.get_name())

    def __eq__(self, other):
        return isinstance(other, ReferencableInterface) and other.get_name() == self.get_name()

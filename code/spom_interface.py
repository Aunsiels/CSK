class SPOMInterface(object):
    """SPOMInterface
    Represents a SPOM member
    """

    def get(self):
        """get
        Gives the value of the SPOM
        :return: the value
        :rtype: str
        """
        raise NotImplementedError

    def __str__(self):
        return str(self.get())

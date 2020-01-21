from .spom_interface import SPOMInterface


class PredicateInterface(SPOMInterface):
    """PredicateInterface
    Represents a predicate
    """

    def __init__(self):
        self._predicate = ""

    def get(self):
        return self._predicate

from quasimodo.serializable import Serializable
from .predicate_interface import PredicateInterface


class Predicate(PredicateInterface, Serializable):
    """Predicate
    Default implementation of a PredicateInterface
    """

    def to_dict(self):
        res = dict()
        res["type"] = "Predicate"
        res["value"] = self.get()
        return res

    def __init__(self, predicate):
        super().__init__()
        self._predicate = predicate

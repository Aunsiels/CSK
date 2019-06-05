from .predicate_interface import PredicateInterface


class Predicate(PredicateInterface):
    """Predicate
    Default implementation of a PredicateInterface
    """

    def __init__(self, predicate):
        super().__init__()
        self._predicate = predicate

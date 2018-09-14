from fact_interface import FactInterface

class Fact(FactInterface):
    """Fact
    The default implementation of FactInterface
    """

    def __init__(subject,
                 predicate,
                 obj,
                 negative=False,
                 modality=None):
        self._subject = subject
        self._predicate = predicate
        self._object = obj
        self._negative = negative
        self._modality = modality

from generated_fact_interface import GeneratedFactInterface
from subject import Subject
from object import Object
from predicate import Predicate
from modality import Modality

class GeneratedFact(GeneratedFactInterface):
    """GeneratedFact
    The default implementation of GeneratedFactInterface
    """

    def __init__(self,
                 subject,
                 predicate,
                 obj,
                 modality,
                 negative,
                 score,
                 sentence_source,
                 module_source,
                 submodule_source,
                 pattern=None):
        if type(subject) == str:
            self._subject = Subject(subject)
        else:
            self._subject = subject # SubjectInterface
        if type(predicate) == str:
            self._predicate = Predicate(predicate)
        else:
            self._predicate = predicate # PredicateInterface
        if type(obj) == str:
            self._object = Object(obj)
        else:
            self._object = obj # ObjectInterface
        if type(modality) == str:
            self._modality = Modality(modality)
        else:
            self._modality = modality # Optinal ModalityInterface
        self._negative = negative
        self._score = score
        self._sentence_source = sentence_source
        self._module_source = module_source
        self._submodule_source = submodule_source
        self._pattern = pattern

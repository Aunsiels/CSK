from fact_interface import FactInterface
from subject import Subject
from object import Object
from predicate import Predicate
from modality import Modality

class Fact(FactInterface):
    """Fact
    The default implementation of FactInterface
    """

    def __init__(self,
                 subject,
                 predicate,
                 obj,
                 negative=False,
                 modality=None):
        if type(subject) == str:
            self._subject = Subject(subject)
        else:
            self._subject = subject
        if type(predicate) == str:
            self._predicate = Predicate(predicate)
        else:
            self._predicate = predicate
        if type(obj) == str:
            self._object = Object(obj)
        else:
            self._object = obj
        self._negative = negative
        if type(modality) == str:
            self._modality = Modality(modality)
        else:
            self._modality = modality

    def change_subject(self, new_subject):
        return Fact(new_subject,
                    self.get_predicate(),
                    self.get_object(),
                    self.is_negative(),
                    self.get_modality())

    def change_predicate(self, new_predicate):
        return Fact(self.get_subject(),
                    new_predicate,
                    self.get_object(),
                    self.is_negative(),
                    self.get_modality())

    def change_object(self, new_object):
        return Fact(self.get_subject(),
                    self.get_predicate(),
                    new_object,
                    self.is_negative(),
                    self.get_modality())

    def change_modality(self, new_modality):
        return Fact(self.get_subject(),
                    self.get_predicate(),
                    self.get_object(),
                    self.is_negative(),
                    new_modality)

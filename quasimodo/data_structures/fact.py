from quasimodo.serializable import Serializable
from quasimodo.statement_maker import correct_statement, NEGATE_VERB
from .fact_interface import FactInterface
from .subject import Subject
from .object import Object
from .predicate import Predicate
from .modality import Modality


class Fact(FactInterface, Serializable):
    """Fact
    The default implementation of FactInterface
    """

    def to_dict(self):
        res = dict()
        res["type"] = "Fact"
        res["subject"] = self._subject.to_dict()
        res["predicate"] = self._predicate.to_dict()
        res["object"] = self._object.to_dict()
        if self._modality is not None:
            res["modality"] = self._modality.to_dict()
        else:
            res["modality"] = {"type": "NO_MODALITY"}
        res["negative"] = self._negative
        return res

    def __init__(self, subject, predicate, obj, modality=None, negative=False):
        super().__init__()
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
        if modality is None:
            self._modality = Modality()
        elif type(modality) == str:
            self._modality = Modality(modality)
        else:
            self._modality = modality

    def change_subject(self, new_subject):
        return Fact(new_subject,
                    self.get_predicate(),
                    self.get_object(),
                    self.get_modality(),
                    self.is_negative())

    def change_predicate(self, new_predicate):
        return Fact(self.get_subject(),
                    new_predicate,
                    self.get_object(),
                    self.get_modality(),
                    self.is_negative())

    def change_object(self, new_object):
        return Fact(self.get_subject(),
                    self.get_predicate(),
                    new_object,
                    self.get_modality(),
                    self.is_negative())

    def change_modality(self, new_modality):
        return Fact(self.get_subject(),
                    self.get_predicate(),
                    self.get_object(),
                    new_modality,
                    self.is_negative())

    def to_sentence(self):
        subject = self.get_subject().get_plural()
        predicate = self.get_predicate().get_natural_representation()
        obj = str(self.get_object())
        normal_modality = self.get_modality().get_normal_modalities()
        if normal_modality:
            normal_modality = "[" + normal_modality + "] "
        some_modality = self.get_modality().get_some_modalities()
        if some_modality:
            some_modality = "(" + some_modality + ") "
        if self.is_negative():
            if predicate in NEGATE_VERB:
                predicate += " not"
            elif predicate == "can":
                predicate += "not"
            elif predicate.startswith("are "):
                predicate = "are not " + predicate[3:]
            else:
                predicate = "do not " + predicate
        return correct_statement(some_modality + subject + " " + predicate + " " + normal_modality + obj)

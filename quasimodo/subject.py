from quasimodo.statement_maker import _plural_engine

from quasimodo.serializable import Serializable
from .subject_interface import SubjectInterface


class Subject(SubjectInterface, Serializable):
    """Subject
    Default implementation fo the SubjectInterface
    """

    def to_dict(self):
        res = dict()
        res["type"] = "Subject"
        res["value"] = self.get()
        return res

    def __init__(self, subject):
        super().__init__()
        self._subject = subject

    def get_plural(self):
        return _plural_engine.plural(self.get())

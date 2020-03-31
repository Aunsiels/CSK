from quasimodo.serializable import Serializable
from .subject_interface import SubjectInterface
from ..inflect_accessor import DEFAULT_INFLECT


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
        return DEFAULT_INFLECT.to_plural(self.get())

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

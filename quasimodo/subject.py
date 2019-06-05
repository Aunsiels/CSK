from .subject_interface import SubjectInterface


class Subject(SubjectInterface):
    """Subject
    Default implementation fo the SubjectInterface
    """

    def __init__(self, subject):
        super().__init__()
        self._subject = subject

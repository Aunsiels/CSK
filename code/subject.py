from subject_interface import SubjectInterface

class Subject(SubjectInterface):
    """Subject
    Default implementation fo the SubjectInterface
    """

    def __init__(self, subject):
        self._subject = subject

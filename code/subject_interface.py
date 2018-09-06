from spom_interface import SPOMInterface

class SubjectInterface(SPOMInterface):
    """SubjectInterface
    Represents a subject
    """

    def __init__(self):
        self._subject = ""

    def get(self):
        return self._subject

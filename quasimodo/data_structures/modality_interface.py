from .spom_interface import SPOMInterface


class ModalityInterface(SPOMInterface):
    """ModalityInterface
    Represents a modality
    """

    def __init__(self):
        self._modality = ""

    def get(self):
        return self._modality


from modality_interface import ModalityInterface

class Modality(ModalityInterface):
    """Modality
    The default implementation of the ModalityInterface
    """

    def __init__(self, modality):
        self._modality = modality

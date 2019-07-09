from quasimodo.serializable import Serializable
from .modality_interface import ModalityInterface


class Modality(ModalityInterface, Serializable):
    """Modality
    The default implementation of the ModalityInterface
    """

    def to_dict(self):
        res = dict()
        res["type"] = "Modality"
        res["value"] = self.get()
        return res

    def __init__(self, modality):
        super().__init__()
        self._modality = modality

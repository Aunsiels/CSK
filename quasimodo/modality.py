from quasimodo.serializable import Serializable
from .modality_interface import ModalityInterface


def get_multiple_parts_combination(sentence_score_pairs):
    return " // ".join([x[0] + " x#x" + str(x[1])
                        for x in sentence_score_pairs
                        if x[0] != ""])


def read_sentence(sentence):
    res = []
    sentence_parts = sentence.split(" // ")
    for part in sentence_parts:
        part_score = part.split("x#x")
        if len(part_score) == 1:
            res.append((part_score[0].strip(), 1))
        else:
            res.append((part_score[0].strip(), int(part_score[1])))
    return res


class Modality(ModalityInterface, Serializable):
    """Modality
    The default implementation of the ModalityInterface
    """

    def to_dict(self):
        res = dict()
        res["type"] = "Modality"
        res["value"] = self.get()
        return res

    def __init__(self, modality=""):
        super().__init__()
        self._modality = modality

    def get_modalities_and_scores(self):
        return read_sentence(self.get())

    def is_empty(self):
        return len(self.get()) == 0

    def contains_completing_part(self):
        return "TBC" in self.get()

    def get_number_completing_parts(self):
        return self.get().count("TBC")

    @staticmethod
    def from_modalities_and_scores(modality_score_pairs):
        raw_modality = get_multiple_parts_combination(modality_score_pairs)
        return Modality(raw_modality)

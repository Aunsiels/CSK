from quasimodo.parameters_reader import ParametersReader
from quasimodo.assertion_validation.sentence_comparator import SentenceComparator

parameters_reader = ParametersReader()
CONCEPTUAL_CAPTION_FILE = parameters_reader.get_parameter("conceptual-caption-file") or ""


class ConceptualCaptionsComparatorSubmodule(SentenceComparator):

    def __init__(self, module_reference):
        super().__init__(module_reference, CONCEPTUAL_CAPTION_FILE)
        self._name = "Conceptual Caption"

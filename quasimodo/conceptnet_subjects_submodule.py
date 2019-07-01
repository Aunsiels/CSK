import os

from quasimodo.subject_file_submodule import SubjectFileSubmodule
from quasimodo.parameters_reader import ParametersReader


parameters_reader = ParametersReader()
FILENAME = parameters_reader.get_parameter("subjects_20k") or \
        os.path.dirname(__file__) + "/data/conceptnet_subjects.txt"


class ConceptnetSubjectsSubmodule(SubjectFileSubmodule):

    def __init__(self, module_reference):
        super().__init__(module_reference)
        self._module_reference = module_reference
        self._name = "Conceptnet Subject Seeds"
        self._filename = FILENAME

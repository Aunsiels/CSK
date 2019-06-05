from .subject_file_submodule import SubjectFileSubmodule
import os


class ConceptnetSubjectsSubmodule(SubjectFileSubmodule):

    def __init__(self, module_reference):
        super().__init__(module_reference)
        self._module_reference = module_reference
        self._name = "Conceptnet Subject Seeds"
        self._filename = os.path.dirname(__file__) + "/data/subjects_20k.txt"

from .subject_file_submodule import SubjectFileSubmodule
import os


class OccupationsSubmodule(SubjectFileSubmodule):

    def __init__(self, module_reference):
        self._module_reference = module_reference
        self._name = "Occupation Seeds"
        self._filename = os.path.dirname(__file__) + "/data/occupations_50.txt"

import os
from quasimodo.seeds.subject_file_submodule import SubjectFileSubmodule
from quasimodo.parameters_reader import ParametersReader


parameters_reader = ParametersReader()
FILENAME = parameters_reader.get_parameter("occupations-subjects") or \
        os.path.dirname(__file__) + "/data/occupations_50.txt"


class OccupationsSubmodule(SubjectFileSubmodule):

    def __init__(self, module_reference):
        self._module_reference = module_reference
        self._name = "Occupation Seeds"
        self._filename = FILENAME

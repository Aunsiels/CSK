import os
from .subject_file_submodule import SubjectFileSubmodule


class AnimalSubmodule(SubjectFileSubmodule):
    """AnimalSubmodule
    A submodule to produce animals of the subjects of the input
    """

    def __init__(self, module_reference):
        super().__init__(module_reference)
        self._module_reference = module_reference
        self._name = "Animal Seeds"
        self._filename = os.path.dirname(__file__) + "/data/anitemp.txt"

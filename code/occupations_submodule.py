from subject_file_submodule import SubjectFileSubmodule

class OccupationsSubmodule(SubjectFileSubmodule):

    def __init__(self, module_reference):
        self._module_reference = module_reference
        self._name = "Occupation Seeds"
        self._filename = "data/occupations.csv"

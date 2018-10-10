from subject_file_submodule import SubjectFileSubmodule


class ConceptnetSubjectsSubmodule(SubjectFileSubmodule):

    def __init__(self, module_reference):
        self._module_reference = module_reference
        self._name = "Conceptnet Subject Seeds"
        self._filename = "data/xaj"

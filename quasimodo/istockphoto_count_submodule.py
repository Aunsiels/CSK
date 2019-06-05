from .archit_submodule import ArchitSubmodule


class IstockphotoCountSubmodule(ArchitSubmodule):

    def __init__(self, module_reference):
        super().__init__(module_reference)
        self._name = "Istockphoto count"
        self._index = 11

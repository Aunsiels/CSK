from archit_submodule import ArchitSubmodule

class PinterestCountSubmodule(ArchitSubmodule):

    def __init__(self, module_reference):
        super().__init__(module_reference)
        self._name = "Pinterest count"
        self._index = 9

from .archit_submodule import ArchitSubmodule


class PinterestRegressionSubmodule(ArchitSubmodule):

    def __init__(self, module_reference):
        super().__init__(module_reference)
        self._name = "Pinterest regression"
        self._index = 10

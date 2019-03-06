from archit_submodule import ArchitSubmodule

class IstockphotoRegressionSubmodule(ArchitSubmodule):

    def __init__(self, module_reference):
        super().__init__(module_reference)
        self._name = "Istockphoto regression"
        self._index = 12

from quasimodo.web_search.archit_submodule import ArchitSubmodule


class WebCountSubmodule(ArchitSubmodule):

    def __init__(self, module_reference):
        super().__init__(module_reference)
        self._name = "Web count"
        self._index = 3

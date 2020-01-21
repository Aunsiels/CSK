from quasimodo.web_search.archit_submodule import ArchitSubmodule


class YoutubeRegressionSubmodule(ArchitSubmodule):

    def __init__(self, module_reference):
        super().__init__(module_reference)
        self._name = "Youtube regression"
        self._index = 6

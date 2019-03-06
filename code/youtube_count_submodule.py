from archit_submodule import ArchitSubmodule

class YoutubeCountSubmodule(ArchitSubmodule):

    def __init__(self, module_reference):
        super().__init__(module_reference)
        self._name = "Youtube count"
        self._index = 5

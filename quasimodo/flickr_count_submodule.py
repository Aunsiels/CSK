from .archit_submodule import ArchitSubmodule


class FlickrCountSubmodule(ArchitSubmodule):

    def __init__(self, module_reference):
        super().__init__(module_reference)
        self._name = "Flickr count"
        self._index = 7


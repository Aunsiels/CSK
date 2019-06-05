from .archit_submodule import ArchitSubmodule


class FlickrRegressionSubmodule(ArchitSubmodule):

    def __init__(self, module_reference):
        super().__init__(module_reference)
        self._name = "Flickr regression"
        self._index = 8

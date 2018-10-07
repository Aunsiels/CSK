from wikipedia_cooccurrence_submodule import WikipediaCooccurrenceSubmodule
import os

class SimpleWikipediaCooccurrenceSubmodule(WikipediaCooccurrenceSubmodule):

    def __init__(self, module_reference):
        self._module_reference = module_reference
        self._name = "Simple Wikipedia Cooccurrence"
        self._cache_dir = "wikipedia-cache-simple/"
        self._lang = "simple"
        if not os.path.exists(self._cache_dir):
            os.makedirs(self._cache_dir)

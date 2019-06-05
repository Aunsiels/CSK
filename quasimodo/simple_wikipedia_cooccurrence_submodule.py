from .wikipedia_cooccurrence_submodule import WikipediaCooccurrenceSubmodule


class SimpleWikipediaCooccurrenceSubmodule(WikipediaCooccurrenceSubmodule):

    def __init__(self, module_reference, use_cache=True, cache_name="simple-wikipedia-cache"):
        super().__init__(module_reference, use_cache, cache_name)
        self._module_reference = module_reference
        self._name = "Simple Wikipedia Cooccurrence"
        self._lang = "simple"

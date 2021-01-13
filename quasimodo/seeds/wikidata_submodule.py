import os
from quasimodo.seeds.subject_file_submodule import SubjectFileSubmodule
from quasimodo.parameters_reader import ParametersReader


parameters_reader = ParametersReader()
FILENAME = parameters_reader.get_parameter("wikidata-subjects") or \
        os.path.dirname(__file__) + "/data/wikidata.txt"


class WikidataSubmodule(SubjectFileSubmodule):
    """WikidataSubmodule
    A submodule to produce wikidatas of the subjects of the input
    """

    def __init__(self, module_reference):
        super().__init__(module_reference)
        self._module_reference = module_reference
        self._name = "Wikidata Seeds"
        self._filename = FILENAME

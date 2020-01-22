from quasimodo.parameters_reader import ParametersReader
from quasimodo.assertion_validation.association_submodule import AssociationSubmodule
import os.path
import pickle

parameters_reader = ParametersReader()
filename = parameters_reader.get_parameter("imagetag-associations") or ""

CACHE_IMAGETAG = "cache_imagetag.pck"


class ImagetagSubmodule(AssociationSubmodule):

    def __init__(self, module_reference):
        super().__init__(module_reference)
        self._module_reference = module_reference
        self._name = "Image Tag submodule"

    def _get_associations(self, subjects):
        associations = dict()
        if os.path.isfile(CACHE_IMAGETAG):
            return pickle.load(open(CACHE_IMAGETAG, "rb"))
        with open(filename) as f:
            for line in f:
                line = line.strip().lower().split("\t")
                for word0 in line:
                    if word0 not in associations:
                        associations[word0] = dict()
                    assos_word0 = associations[word0]
                    for word1 in line:
                        if word0 == word1:
                            continue
                        assos_word0[word1] = assos_word0.get(word1, 0) + 1
        pickle.dump(associations, open(CACHE_IMAGETAG, "wb"))
        return associations

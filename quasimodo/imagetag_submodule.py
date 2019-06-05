from quasimodo.parameters_reader import ParametersReader
from .association_submodule import AssociationSubmodule

parameters_reader = ParametersReader()
filename = parameters_reader.get_parameter("imagetag-associations") or ""


class ImagetagSubmodule(AssociationSubmodule):

    def __init__(self, module_reference):
        super().__init__(module_reference)
        self._module_reference = module_reference
        self._name = "Image Tag submodule"

    def _get_associations(self, subjects):
        associations = dict()
        with open(filename) as f:
            for line in f:
                line = line.strip().lower().split("\t")
                for word0 in line:
                    for word1 in line:
                        if word0 == word1:
                            continue
                        if word0 in associations:
                            associations[word0][word1] = associations[word0].setdefault(word1, 0) + 1
                        else:
                            associations[word0] = dict()
                            associations[word0][word1] = 1
        return associations

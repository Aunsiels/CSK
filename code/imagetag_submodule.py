from association_submodule import AssociationSubmodule
import logging

filename = "/media/julien/7dc04770-227b-40fd-a591-c8e0c3a71a37/commonsense_data/assos_imagestags_openimage.tsv"

class ImagetagSubmodule(AssociationSubmodule):

    def __init__(self, module_reference):
        self._module_reference = module_reference
        self._name = "Image Tag submodule"

    def _get_assos(self, subjects):
        d = dict()
        subjects = set([x.get() for x in subjects])
        with open(filename) as f:
            for line in f:
                line = line.strip().lower().split("\t")
                for s0 in line:
                    if s0 not in subjects:
                        continue
                    for s1 in line:
                        if s0 == s1:
                            continue
                        if s0 in d:
                            d[s0][s1] = d[s0].setdefault(s1, 0) + 1
                        else:
                            d[s0] = dict()
                            d[s0][s1] = 1
        return d

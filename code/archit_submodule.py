import logging

from submodule_interface import SubmoduleInterface
from generated_fact import GeneratedFact

filename = "data/anioccu_all.tsv"

class ArchitSubmodule(SubmoduleInterface):

    def __init__(self, module_reference):
        self._module_reference = module_reference
        self._name = "Archit submodule" # To redefine
        self._index = -1 # column of the feature

    def process(self, input_interface):
        logging.info("Start the " + self._name + " archit submodule")
        first = True
        spos = set()
        for gf in input_interface.get_generated_facts():
            spos.add((gf.get_subject().get(),
                      gf.get_predicate().get(),
                      gf.get_object().get()))
        new_gfs = []
        with open(filename) as f:
            for line in f:
                if first:
                    first = False
                    continue
                line = line.strip().split("\t")
                subj = line[0]
                pred = line[1]
                obj = line[2]
                if (subj, pred, obj) not in spos:
                    continue
                score = float(line[self._index])
                if score == 0:
                    continue
                new_gfs.append(
                    GeneratedFact(
                        subj,
                        pred,
                        obj,
                        "",
                        0,
                        score,
                        "",
                        self._module_reference,
                        self))
        return input_interface.add_generated_facts(new_gfs)

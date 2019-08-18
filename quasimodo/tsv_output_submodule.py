import os
import re

from quasimodo.parameters_reader import ParametersReader
from .submodule_interface import SubmoduleInterface
import logging


parameters_reader = ParametersReader()
OUT_DIR = parameters_reader.get_parameter("out-dir") or os.path.dirname(__file__) + "/out/"


def get_version():
    version = 1
    regex_output = re.compile("quasimodo(?P<version>\d+).tsv")
    for file in os.listdir(OUT_DIR):
        match = regex_output.match(file)
        if match is not None:
            version = max(version, int(match.group("version")) + 1)
    return version


def get_all_triples_as_tsv(input_interface):
    triples = []
    for generated_fact in input_interface.get_generated_facts():
        triples.append(generated_fact.get_tsv())
    return triples


def save_tsv_triples(triples):
    version = get_version()
    save_file = OUT_DIR + "quasimodo" + str(version) + ".tsv"
    with open(save_file, "w") as f:
        f.write("\t".join(["subject", "predicate", "object", "modality", "is_negative", "score", "sentences source"]) + "\n")
        f.write("\n".join(triples))


class TSVOutputSubmodule(SubmoduleInterface):

    def __init__(self, module_reference):
        super().__init__()
        self._module_reference = module_reference
        self._name = "TSV Output"

    def process(self, input_interface):
        logging.info("Start TSV output submodule")
        triples = get_all_triples_as_tsv(input_interface)
        save_tsv_triples(triples)
        return input_interface

import logging
import os

from quasimodo.spacy_accessor import get_default_annotator
from quasimodo.data_structures.submodule_interface import SubmoduleInterface
from quasimodo.parameters_reader import ParametersReader


parameters_reader = ParametersReader()
path_to_properties = parameters_reader.get_parameter("properties-dir") or ""


class AreTransformationSubmodule(SubmoduleInterface):

    def __init__(self, module_reference):
        super().__init__()
        self._module_reference = module_reference
        self._name = "Are transformation"

    def process(self, input_interface):
        logging.info("Start the are predicate transformation")
        gfs = input_interface.get_generated_facts()
        conversion = dict()
        for filename in os.listdir(path_to_properties):
            name = "has_" + filename.replace(".txt", "")
            with open(path_to_properties + filename) as f:
                for line in f:
                    line = line.strip()
                    conversion[line] = name
        new_gfs = []
        for gf in gfs:
            predicate = gf.get_predicate().get()
            obj = gf.get_object().get()
            if predicate in ["be", "are", "is", "hasProperty", "have", "has"]:
                if obj in conversion:
                    new_gf = gf.change_predicate(conversion[obj])
                else:
                    spacy_annotator = get_default_annotator()
                    obj_lemmatized = " ".join(spacy_annotator.lemmatize(obj))
                    if obj_lemmatized in conversion:
                        new_gf = gf.change_predicate(conversion[obj_lemmatized])
                    elif gf.get_pattern() is not None and gf.get_pattern().get_relation() is not None:
                        new_gf = gf.change_predicate(gf.get_pattern().get_relation())
                    else:
                        new_gf = gf
            else:
                new_gf = gf
            new_gfs.append(new_gf)
        return input_interface.replace_generated_facts(new_gfs)

from quasimodo.data_structures.module_interface import ModuleInterface
from quasimodo.default_submodule_factory import DefaultSubmoduleFactory
import logging
import objgraph


class AssertionNormalizationModule(ModuleInterface):
    """AssertionNormalizationModule
    A class to normalize the assertion generated by other modules
    """

    def __init__(self):
        module_names = ["lower-case",
                        "clean-subject",
                        "only-subject",
                        "no-personal",
                        "filter-object",
                        "cleaning-predicate",
                        "singular-subject",
                        "basic-modality",
                        "present-continuous",
                        "are-transformation",
                        "can-transformation",
                        "be-normalization",
                        "identical-subj-obj",
                        "present-conjugate",
                        "similar-object-remover",
                        "filter-language-questions",
                        "fact-combinor",
                        "tbc-cleaner"
                        ]
        super(AssertionNormalizationModule, self).__init__(
            module_names, DefaultSubmoduleFactory())
        self._name = "Assertion Normalization Module"

    def process(self, input_interface):
        logging.info("Start the assertion normalization module")
        for submodule in self._submodules:
            input_interface = submodule.process(input_interface)
            logging.info("We have " + str(len(
                input_interface.get_generated_facts())) + " facts.")
            if "beach" in input_interface.get_subjects():
                logging.info("beach is a subject")
            else:
                logging.info("beach is not a subject")
            if contains_beach_have_sand(input_interface.get_generated_facts()):
                logging.info("Still beach have sand")
            else:
                logging.info("Beach have sand disappeared")
            if len(input_interface.get_generated_facts()) > 0:
                logging.info("The first fact is: " + str(input_interface.get_generated_facts()[0]))
            submodule.clean()
        return input_interface


def contains_beach_have_sand(gfs):
    for gf in gfs:
        if ((gf.get_subject().get() == "beach" or gf.get_subject().get() == "beaches")
           and (gf.get_predicate().get() == "have" or gf.get_predicate().get() == "has")
           and gf.get_object().get() == "sand"):
            return True
    return False

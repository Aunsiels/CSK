from quasimodo.data_structures.module_interface import ModuleInterface
from quasimodo.default_submodule_factory import DefaultSubmoduleFactory
import logging
import objgraph


class AssertionValidationModule(ModuleInterface):
    """AssertionValidationModule
    A module which valides assertions, i.e. given an assertion, give a new score
    to it.
    """

    def __init__(self):
        module_names = [
                        "google-book",
                        "flickr-clusters",
                        "imagetag",
                        "wikipedia-cooccurrence",
                        "simple-wikipedia-cooccurrence",
                        "conceptual-captions",
                        "what-questions"
                        ]
        super(AssertionValidationModule, self).__init__(
            module_names, DefaultSubmoduleFactory())
        self._name = "Assertion Validation Module"

    def process(self, input_interface):
        logging.info("Start the assertion validation module")
        for submodule in self._submodules:
            input_interface = submodule.process(input_interface)
            submodule.clean()
            logging.info(objgraph.growth())
            logging.info(objgraph.most_common_types())
        return input_interface

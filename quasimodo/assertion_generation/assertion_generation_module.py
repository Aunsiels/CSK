from quasimodo.data_structures.module_interface import ModuleInterface
from quasimodo.default_submodule_factory import DefaultSubmoduleFactory
import logging
import objgraph


class AssertionGenerationModule(ModuleInterface):
    """AssertionGenerationModule
    A module which generates assertions
    """

    def __init__(self):
        module_names = [
                        "google-autocomplete",
                        "bing-autocomplete",
                        "yahoo-questions",
                        "answerscom-questions",
                        "quora-questions",
                        "reddit-questions",
                        "fact-combinor"
                        ]
        super(AssertionGenerationModule, self).__init__(
            module_names, DefaultSubmoduleFactory())
        self._name = "Assertion Generation Module"

    def process(self, input_interface):
        logging.info("Start the assertion generation module")
        generated_facts = []
        logging.info(objgraph.growth())
        # For now in sequence, we could make it be parallel
        for submodule in self._submodules:
            input_temp = submodule.process(input_interface)
            generated_facts += input_temp.get_generated_facts()
            submodule.clean()
            logging.info(objgraph.growth())
            logging.info(objgraph.most_common_types())
        return input_interface.add_generated_facts(generated_facts)

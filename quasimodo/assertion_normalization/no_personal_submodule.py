from quasimodo.data_structures.submodule_interface import SubmoduleInterface
import logging


class NoPersonalSubmodule(SubmoduleInterface):

    def __init__(self, module_reference):
        super().__init__()
        self._module_reference = module_reference
        self._name = "No Personal"

    def process(self, input_interface):
        logging.info("Start the removal of personal words")
        personals = ["my", "your", "our", "I", "you", "it", "he", "she", "so",
                     "such", "much", "me", "this", "that", "here", "there",
                     "his", "her", "its"]
        new_generated_facts = list(filter(
            lambda x: not any([y in personals
                               for y in x.get_object().get().split(" ")]),
            input_interface.get_generated_facts()))

        logging.info("%d facts were removed by the personal words cleaner",
                     len(input_interface.get_generated_facts()) - len(new_generated_facts))

        return input_interface.replace_generated_facts(new_generated_facts)

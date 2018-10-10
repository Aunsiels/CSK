from submodule_interface import SubmoduleInterface
import logging


class NoPersonalSubmodule(SubmoduleInterface):

    def __init__(self, module_reference):
        self._module_reference = module_reference
        self._name = "No Personnal"

    def process(self, input_interface):
        logging.info("Start the removal of personal words")
        personals = ["my", "your", "our", "I", "you", "it", "he", "she", "so",
                     "such", "much", "me", "this", "that", "here", "there"]
        new_generated_facts = list(filter(
            lambda x: not any([y in personals
                               for y in x.get_object().get().split(" ")]),
            input_interface.get_generated_facts()))
        return input_interface.replace_generated_facts(new_generated_facts)

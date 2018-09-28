from submodule_interface import SubmoduleInterface
import logging


class FilterObjectSubmodule(SubmoduleInterface):

    def __init__(self, module_reference):
        self._module_reference = module_reference
        self._name = "Filter Object"

    def process(self, input_interface):
        logging.info("Start the filtering object")
        forbidden = ["used", "called"]
        new_generated_facts = list(filter(
            lambda x: x.get_object().get() not in forbidden,
            input_interface.get_generated_facts()))
        return input_interface.replace_generated_facts(new_generated_facts)

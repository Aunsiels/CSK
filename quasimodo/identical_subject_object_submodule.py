from .submodule_interface import SubmoduleInterface
import logging


class IdenticalSubjectObjectSubmodule(SubmoduleInterface):

    def __init__(self, module_reference):
        super().__init__()
        self._module_reference = module_reference
        self._name = "Identical subject/object"

    def process(self, input_interface):
        logging.info("Start the antonym checking")
        new_gfs = [g for g in input_interface.get_generated_facts()
                   if g.get_subject().get() != g.get_object().get()]
        return input_interface.replace_generated_facts(new_gfs)